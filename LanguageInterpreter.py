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
        condition.replace(" = ", " == ")
        condition.replace("ELIF ", "elif ")
        condition.replace("ELSE ", "else ")
        condition.replace("IF ", "if ")
        condition.replace(" AND ", " and ")
        condition.replace(" OR ", " or ")
        condition.replace(" NOT ", " not ")
        condition.replace(" = ", " == ")
        condition.replace(" = ", " == ")
        condition.replace(" = ", " == ")
        
        # allRecords = findall()
        
        return interpretedText
    
    
    
    def __processExecution(self, payload):
        
        parameterList = []
        for parameter in payload.get('params'):
            if parameter.get('pType') == 'reference':
                parameterList.append(parameter.get('pValue'))
            elif parameter.get('pType') == 'value':
                parameterList.append(f"\"{parameter.get('pValue')}\"")
        print(parameterList)
        print(', '.join(parameterList))
        
        interpretedText = ""
        
        if payload.get('alias'):
            interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')} = {payload.get('fName')}(({', '.join(parameterList)}))"
        else:
            interpretedText += "\t" * self.tabsToInclude + f"{payload.get('fName')}({', '.join(parameterList)})"
        
        return interpretedText
    
    
    
    def __processFunction(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"def {payload.get('fName')}({', '.join(payload.get('args'))}):\n"
        self.tabsToInclude += 1
        interpretedText += "\t" * self.tabsToInclude + "localVariables = locals()\n"
        interpretedText += "\t" * self.tabsToInclude + f"exec(anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')}), globals(), localVariables)\n"
        # interpretedText += f"getFunction(\'{payload.get('recordID')}\')\n"
        
        return interpretedText
    
    
    
    def __processIntegration(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Original = anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]"
        
        return interpretedText
    
    
    
    def __processModule(self, payload):
        
        interpretedText = ""
        
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Original = anObject.getIntegrationWithID(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += "\t" * self.tabsToInclude + f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]"
        
        return interpretedText
    
    
    
    def processPayload(self):
        
        for type in self.originalPayload:
            self.recordIterated = []
            process = self.processes[type['type']]
            result = process(type)
            self.interpretedText += result




    
def initialize():
    
    with open('testSample.yml') as stream:
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