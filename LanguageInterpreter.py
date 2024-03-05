from re import findall
from traceback import print_exc
from yaml import safe_load as loadYAML





class YAMLLanguageInterpreter():
    
    def __init__(self, YAMLPayload):
        
        self.originalPayload = loadYAML(YAMLPayload)
        self.interpretedText = ""
        self.interpretedText += """from re import findall
from traceback import print_exc
from yaml import safe_load as loadYAML\n\n\n
"""
        self.recordIterated = []
        
        self.processes = {
            'condition': self.__processCondition, 
            'execution': self.__processExecution, 
            'function': self.__processFunction, 
            'integration': self.__processIntegration, 
            'module': self.__processModule
        }
        self.tabsToInclude = 0
        self.dcitionaryPattern = r'\b(\w+)\[\'(\w+)\'\]'
    
    
    
    def __processCondition(self, payload):
        ...
    
    
    
    def __processExecution(self, payload):
        ...
    
    
    
    def __processFunction(self, payload):
        
        interpretedText = ""
        
        interpretedText += f"{payload.get('name')}({', '.join(payload.get('arguments'))})\n"
        interpretedText += f"getFunction(\'{payload.get('recordID')}\')\n"
        
        return interpretedText
    
    
    
    def __processIntegration(self, payload):
        
        interpretedText = ""
        
        interpretedText += f"{payload.get('alias')}Original = getIntegration(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]"
        
        return interpretedText
    
    
    
    def __processModule(self, payload):
        
        interpretedText = ""
        
        interpretedText += f"{payload.get('alias')}Original = getModule(\'{payload.get('recordID')}\', {payload.get('params')})\n"
        interpretedText += f"{payload.get('alias')}Copy = {payload.get('alias')}Original[:]"
    
    
    
    def processPayload(self):
        
        for type in self.originalPayload:
            self.recordIterated = []
            process = self.processes[type['type']]
            result = process(type)
            self.interpretedText += result




    
def initialize():
    
    with open('test.yaml') as stream:
        anObject = YAMLLanguageInterpreter(stream)
        stream.close()

    anObject.processPayload()
    print(anObject.interpretedText)





if __name__ == '__main__':
    
    try:
        initialize()
    
    except Exception as error:
        print(error)