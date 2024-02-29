from yaml import safe_load as loadYAML





class YAMLLanguageInterpreter():
    
    def __init__(self, YAMLPayload):
        
        self.originalPayload = loadYAML(YAMLPayload)
        self.interpretedText = ''
        self.recordIterated = []
        
        self.processes = {
            'action': self.__processActions, 
            'condition': self.__processConditions, 
            'function': self.__processCodeSnippets, 
            'integration': self.__processIntegrations, 
            'module': self.__processModules
        }
        
    
    
    def __processActions(self, payload):
        print("An action")
    
    
    
    def __processCodeSnippets(self, payload):
        print("A function")
    
    
    
    def __processConditions(self, payload):
        print("A condition")
        return ""
    
    
    
    def __processIntegrations(self, payload):
        
        interpretedText = ''
        if self.interpretedText:
            interpretedText += '\n'
        
        interpretedText += payload.get('alias')
        interpretedText += " = getIntegrationWithID("
        interpretedText += ', '.join(payload.get('parameters'))
        interpretedText += ')'
        
        return interpretedText
    
        
        
    def __processModules(self, payload):
        print("A module")
    
    
    
    def processPayload(self):
                
        for process in self.originalPayload:
            self.recordIterated = []
            action = self.processes[process['type']]
            result = action(process)
            self.interpretedText += result





def initialize():
    
    with open('languageSample.yaml') as stream:
        anObject = YAMLLanguageInterpreter(stream)
        stream.close()
        
    
    anObject.processPayload()
    print(anObject.interpretedText)





if __name__ == '__main__':
    
    try:
        initialize()
        
    except Exception as error:
        print(error)