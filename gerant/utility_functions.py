# we are going to regroup here some functions that we'll help get the job done in the CRUD operations

# function to check if user is allowed in this section 
def is_allowed(request):
    if request.user.is_anonymous:
        return False
    elif request.user.is_friend != True:
        return False
    
    return True
    
    



# this function we'll compact the saison and its name to a string that can be decomposed later
# we can't declare those values separatly inside specific table row because it will make the process more complicated

# the function must also handle an editing operation

def set_saison_name(name, saison_num, actual=None):
    # SAISON_INDEX = int(saison_num) - 1 # to make the num correspond to indexes

    try : 
        # we checked if we already have existing data on the saison
        if actual : 
            previous = str(actual).split('|') # separating the saisons
            
            pair = {}
            for elem in previous:
                if elem == '<end>' :
                    break
                duo = elem.split('-')
                num, nom = duo
                pair[num] = nom # separating the pair of data

        else : pair = {}

        # we set or replace the value at the corresponding index
        pair[saison_num] = name

        # we compact everything into a string
        final_string = ''
        for num in pair :
            # checking if it is the last element
            # else : num, name = elem[0], elem[1]
            name = pair[num]

            final_string += f"{num}-{name}|"

        final_string += '<end>'

        return final_string
        
    except : 
        return False
 
    # return False

