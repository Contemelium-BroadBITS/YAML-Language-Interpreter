from re import findall
from traceback import print_exc
from yaml import safe_load as loadYAML





class YAMLLanguageInterpreter():
    
    def __init__(self, YAMLPayload):
        
        self.originalPayload = YAMLPayload
        self.interpretedText = ''
        self.recordIterated = []
        
        self.processes = {
            'condition': self.__processCondition, 
            'execution': self.__processExecution, 
            'function': self.__processFunction, 
            'integration': self.__processIntegration, 
            'module': self.__processModule
        }
    
    
    
    def __processCondition(self, payload):
        ...
    
    
    
    def __processExecution(self, payload):
        ...
    
    
    
    def __processFunction(self, payload):
        ...
    
    
    
    def __processIntegration(self, payload):
        
        interpretedTExt = ""
    
    
    
    def __processModule(self, payload):
        
        interpretedText = ""
    
    
    
    def processPayload(self):
        
        for type in self.originalPayload:
            self.recordIterated = []
            process = self.processes[type['type']]
            result = process(type)
            self.interpretedText += result




    
def initialize():
    
    with open('languageTestSample.yaml') as stream:
    anObject = YAMLLanguageInterpreter(stream)
    stream.close()
    

anObject.processPayload()
print(anObject.interpretedText)





if __name__ == '__main__':
    
    try:
        initialize()
    
    except Exception as error:
        print(error)