
def getWebsites():
    while True:
        otherWebsite = input("Any other websites? (Leave blank if there are no more websites): ")
        if not otherWebsite:
            return
        yield otherWebsite

def getBulletPoints():
    while True:
        otherBulletPoints = input("Any bullet points to add? (Leave blank if there are no bullet points): ")
        if not otherBulletPoints:
            return
        yield getBulletPoints

def getSubCategories():
    while True:
        otherSubCategories = input("Any subcategories to add? (Leave blank if there are no more subcategories): ")
        if not otherSubCategories:
            return
        
        # call bullet points
        otherSubCategories = list(getBulletPoints())
        yield otherSubCategories

def getCategories():
    while True:
        otherCategories = input("Any categories to add? (Leave blank if there are no more categories): ")
        if not otherCategories:
            return
        
        # call subcategories
        otherCategories = list(getSubCategories())
        yield otherCategories

def buildTexFile(name, linkedin, email, phone, otherWebsites, categories):
    # TODO
    pass

if __name__ == "__main__":
    name = input("What's your name?: ")
    linkedin = input("What's your LinkedIn link?: ")
    email = input("What's your email?: ")
    phone = input("What's your phone number?: ")

    otherWebsites = list(getWebsites())
    categories = list(getCategories())

    print(otherWebsites)