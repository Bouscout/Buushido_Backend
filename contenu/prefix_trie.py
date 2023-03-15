class trienode:
    def __init__(self, word) :
        self.word = word
        self.child = {}
        self.is_end = False
class Trie :
    def __init__(self) :
        self.root = trienode('')
    def insert(self, word):
        node = self.root
        for f in word :
            if f in node.child:
                node = node.child[f]
            else :
                node.child[f] = trienode(f)
                node = node.child[f]
        node.is_end = True
    def adding(self, node, pre):
        if node.is_end == True :
            self.output.append((pre + node.word))
        for child in node.child.values():
            self.adding(child, pre + node.word)

    def search(self, pref):
        node = self.root
        for l in pref:
            if l in node.child:
                node = node.child[l]
            else : 
                return False
        self.output = []
        self.adding(node, pref[:-1])
        return self.output
#let's add all the data 
'''S
every = video.objects.all()
diconame = {}
tr = Trie()
for elem in every:
    diconame[elem.name]=elem.id
    tr.insert(str(elem.name))

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def recherche_ajax(request ):
    print('ajax called bu other laptop ; ', request.GET )
    combi = []
    text = request.GET.get('text')
    print('alors le text est : ', text)
    result = None
    if text:
        result = tr.search(text.capitalize())
        for i in range(len(result)):
            combi.append([result[i], diconame[result[i]]])
    if is_ajax(request=request):
        print(combi)
        return JsonResponse({'seconds':combi}, status=200)
    return render(request, 'recherche.html')
    '''