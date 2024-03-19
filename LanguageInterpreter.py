from re import findall
from traceback import print_exc
from yaml import safe_load as loadYAML



from OpExpertOperations import Interactions





class YAMLLanguageInterpreter():
    
    def __init__(self, YAMLPayload, email, password, URL):
        
        self.originalPayload = loadYAML(YAMLPayload)
        self.interpretedText = ""
        self.interpretedText += "from OpExpertOperations import Interactions\n\n"
        self.interpretedText += f"anObject = Interactions(\'{email}\', \'{password}\', \'{URL}\')\n"
        self.interpretedText += "anObject.login()\n\n"
        self.recordIterated = []
        self.indices = []
        
        self.anObject = Interactions(email, password, URL)
        self.anObject.login()
        
        self.processes = {
            'condition': self.__processCondition, 
            'execute': self.__processExecution, 
            'function': self.__processFunction, 
            'integration': self.__processIntegration, 
            'module': self.__processModule
        }
        self.tabsToInclude = 0
        self.dictionaryPattern = r'\b(\w+)\[\'(\w+)\'\]'
    
    
    
    def __processCondition(self, payload):
        
        interpretedText = ""
        
        condition = payload.get('condition')
        condition = condition.replace(" = ", " == ")
        condition = condition.replace("ELIF ", "elif ")
        condition = condition.replace("ELSE ", "else ")
        condition = condition.replace("IF ", "if ")
        condition = condition.replace(" AND ", " and ")
        condition = condition.replace(" OR ", " or ")
        condition = condition.replace(" NOT ", " not ")
        condition = condition.replace(" = ", " == ")
        condition = condition.replace(" = ", " == ")
        condition = condition.replace(" = ", " == ")
        
        matches = findall(self.dictionaryPattern, condition)
        tabsToInclude = 0
        currentLevel = 0
        if not self.recordIterated:
            interpretedText += '\t' * self.tabsToInclude + "indices = []\n"
        for match in matches:
            if match[0] not in self.recordIterated:
                interpretedText += '\t' * self.tabsToInclude + "indices.append(0)\n"
                interpretedText += "\t" * self.tabsToInclude + f"for {match[0]} in {match[0]}Copy[indices[{currentLevel}]:]:\n"
                self.tabsToInclude += 1
                tabsToInclude += 1
                if currentLevel != len(self.recordIterated) - 1:
                    interpretedText += "\t" * self.tabsToInclude + f"indices[{currentLevel}] += 1\n"
                self.recordIterated.append(match[0])
        interpretedText += "\t" * self.tabsToInclude + f"{condition}:\n"
        self.tabsToInclude += 1
        tabsToInclude += 1
        # interpretedText += "\t" * self.tabsToInclude + f"indices[{currentLevel}] += 1\n"
        for type in payload.get('action'):
                process = self.processes[type['type']]
                interpretedText += process(type)
        if len(self.recordIterated) > 1:
            interpretedText += "\t" * self.tabsToInclude + "break\n"
        self.tabsToInclude -= tabsToInclude
        
        return interpretedText
    
    
    
    def __processExecution(self, payload):
        
        parameterList = []
        for parameter in payload.get('params'):
            if parameter.get('pType') == 'reference':
                parameterList.append(parameter.get('pValue'))
            elif parameter.get('pType') == 'value':
                parameterList.append(f"\"{parameter.get('pValue')}\"")
        
        interpretedText = ""
        
        if payload.get('alias'):
            interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')} = {payload.get('fName')}(({', '.join(parameterList)}))\n"
        else:
            interpretedText += "\t" * self.tabsToInclude + f"{payload.get('fName')}({', '.join(parameterList)})\n"
        
        return interpretedText
    
    
    
    def __processFunction(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"def {payload.get('fName')}"
        if payload.get('args'):
            interpretedText += f"({', '.join(payload.get('args'))}):\n"
        else:
            interpretedText += "():\n"
        
        self.tabsToInclude += 1
        
        for codeLine in self.anObject.getCodeSnippetWithID(payload.get('recordID')).split('\n'):
            interpretedText += "\t" * self.tabsToInclude + codeLine + '\n'
        self.tabsToInclude -= 1
        
        return interpretedText
    
    
    
    def __processIntegration(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Original = anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]\n"
        
        return interpretedText
    
    
    
    def __processModule(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')} = anObject.getModuleWithID(\'{payload.get('recordID')}\', \'{payload.get('moduleName')}\', {payload.get('fields')}, {payload.get('params')})\n"
        
        return interpretedText
    
    
    
    def processPayload(self):
        
        for type in self.originalPayload:
            self.recordIterated = []
            self.indices = []
            process = self.processes[type['type']]
            result = process(type)
            self.interpretedText += result