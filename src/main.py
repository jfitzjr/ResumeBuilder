
def getWebsites():
    while True:
        otherWebsite = input("Any other websites? (Leave blank if there are no more websites): ")
        if not otherWebsite:
            return
        yield otherWebsite

def getBulletPoints():
    while True:
        # TODO
        pass

def getSubCategories():
    while True:
        # TODO 
        pass

def getCategories():
    while True:
        # TODO
        pass

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