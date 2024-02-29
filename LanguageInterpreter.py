from re import findall
from traceback import print_exc
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
        self.tabsToInclude = 0
        self.dcitionaryPattern = r'\b(\w+)\[\'(\w+)\'\]'
        
    
    
    def __processActions(self, payload):
        
        interpretedText = '\n'
        
        if payload.get('alias') != 'false':
            interpretedText += '\t' * self.tabsToInclude + payload.get('alias')
            interpretedText += " = getIntegrationWithID("
            interpretedText += ', '.join("'" + str(parameter) + "'" for parameter in payload.get('parameters'))
            interpretedText += ')'
            interpretedText += '\n' + '\t' * self.tabsToInclude + payload.get('alias') + "Original = " + payload.get('alias') + '[:]\n'
        else:
            interpretedText += '\t' * self.tabsToInclude + payload.get('task') + "("
            interpretedText += ', '.join("'" + str(parameter) + "'" for parameter in payload.get('parameters'))
            interpretedText += ')\n'
        
        return interpretedText
    
    
    
    def __processCodeSnippets(self, payload):
        return "A function"
    
    
    
    def __processConditions(self, payload):
        
        interpretedText = '\n'
        matches = findall(self.dcitionaryPattern, payload.get('condition'))
        whileTabsAddedThisRound = 0
        ifTabsAddedThisRound = 0
        for match in matches:
            if match[0] not in self.recordIterated:
                # rem to append the record at start of loop, and remove record at end of loop
                interpretedText += '\t' * self.tabsToInclude + "while " + match[0] + "Looper < " + match[0] + "Original:\n"
                self.tabsToInclude += 1
                whileTabsAddedThisRound += 1
                interpretedText += '\t' * self.tabsToInclude + match[0] + " = " + match[0] + "Original[" + match[0] + "Looper]\n"
                self.recordIterated.append(match[0])
            ifTabsAddedThisRound += 1
            condition = payload.get('condition').replace(' = ', ' == ').replace(' NOT ', ' not ').replace('ELIF ', 'elif ').replace('IF ', 'if ').replace('ELSE ', 'else ').replace(' AND ', ' and ').replace(' OR ', ' or ') + ":"
            interpretedText += '\t' * self.tabsToInclude + condition
            self.tabsToInclude += 1
            try:
                for process in payload.get('action'):
                    action = self.processes[process['type']]
                    interpretedText += action(process)
                self.tabsToInclude -= 1
            except Exception as error:
                print_exc()
            # self.tabsToInclude -= ifTabsAddedThisRound
        
        try:
            for match in matches:
                # self.recordIterated.remove(match[0])
                ...
        except Exception as error:
            print_exc()
        self.tabsToInclude -= whileTabsAddedThisRound
        
        return interpretedText
        
    
    
    
    def __processIntegrations(self, payload):
        
        interpretedText = '\n'
        
        interpretedText += '\t' * self.tabsToInclude + payload.get('alias')
        interpretedText += " = getIntegrationWithID("
        interpretedText += ', '.join(payload.get('parameters'))
        interpretedText += ')'
        interpretedText += '\n' + '\t' * self.tabsToInclude + payload.get('alias') + "Original = " + payload.get('alias') + '[:]\n'
        
        return interpretedText
    
        
        
    def __processModules(self, payload):
        
        interpretedText = '\n'
        
        interpretedText += '\t' * self.tabsToInclude + payload.get('alias')
        interpretedText += " = getModuleWithID("
        interpretedText += ', '.join(payload.get('parameters'))
        interpretedText += ')'
        interpretedText += '\n' + '\t' * self.tabsToInclude + payload.get('alias') + "Original = " + payload.get('alias') + '[:]\n'
        
        return interpretedText
    
    
    
    def processPayload(self):
                
        for process in self.originalPayload:
            self.recordIterated = []
            action = self.processes[process['type']]
            result = action(process)
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