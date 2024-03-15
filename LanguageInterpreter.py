from re import findall
from traceback import print_exc
from yaml import safe_load as loadYAML



from OpExpertOperations import Interactions





class YAMLLanguageInterpreter():
    
    def __init__(self, YAMLPayload):
        
        self.originalPayload = loadYAML(YAMLPayload)
        self.interpretedText = ""
        self.interpretedText += """from re import findall
from traceback import print_exc
from yaml import safe_load as loadYAML

from OpExpertOperations import Interactions
\n\n\n
"""
        self.recordIterated = []
        
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
        iteratedMatch = []
        indices = []
        for match in matches:
            if match[0] not in iteratedMatch:
                # interpretedText += "\t" * self.tabsToInclude + f"{match[0]}StartIndex = 0\n"
                indices.append('0')
                iteratedMatch.append(match[0])
        interpretedText += "\t" * self.tabsToInclude + f"indices = [{', '.join(indices)}]\n"
        # interpretedText += "\t" * self.tabsToInclude + f"currentLevel = 0\n"
        currentLevel = 0
        iteratedMatch = []
        for match in matches:
            if match[0] not in iteratedMatch:
                interpretedText += "\t" * self.tabsToInclude + f"for {match[0]} in {match[0]}Copy[indices[{currentLevel}]:]:\n"
                self.tabsToInclude += 1
                tabsToInclude += 1
                if currentLevel != len(indices) - 1:
                    # interpretedText += "\t" * self.tabsToInclude + f"{match[0]}StartIndex += 1\n"
                    interpretedText += "\t" * self.tabsToInclude + f"indices[{currentLevel}] += 1\n"
                iteratedMatch.append(match[0])
                currentLevel += 1
        interpretedText += "\t" * self.tabsToInclude + f"{condition}:\n"
        self.tabsToInclude += 1
        tabsToInclude += 1
        interpretedText += "\t" * self.tabsToInclude + f"indices[{currentLevel - 1}] += 1\n"
        for type in payload.get('action'):
            process = self.processes[type['type']]
            interpretedText += process(type)
        if len(indices) > 1:
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
        
        interpretedText += "\t" * self.tabsToInclude + f"def {payload.get('fName')}({', '.join(payload.get('args'))}):\n"
        self.tabsToInclude += 1
        interpretedText += "\t" * self.tabsToInclude + "localVariables = locals()\n"
        interpretedText += "\t" * self.tabsToInclude + f"exec(anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')}), globals(), localVariables)\n"
        # interpretedText += f"getFunction(\'{payload.get('recordID')}\')\n"
        self.tabsToInclude -= 1
        
        return interpretedText
    
    
    
    def __processIntegration(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Original = anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]\n"
        
        return interpretedText
    
    
    
    def __processModule(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Original = anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]\n"
        
        return interpretedText
    
    
    
    def processPayload(self):
        
        for type in self.originalPayload:
            self.recordIterated = []
            process = self.processes[type['type']]
            result = process(type)
            self.interpretedText += result




    
def initialize():
    
    with open('finalized_sample_2.yaml') as stream:
        anObject = YAMLLanguageInterpreter(stream)
        stream.close()

    anObject.processPayload()
    # anObject.interpretedText += "\nprint(theReportCopy)"
    print(anObject.interpretedText)
    # exec(anObject.interpretedText)




if __name__ == '__main__':
    
    try:
        initialize()
    
    except Exception as error:
        print(error)