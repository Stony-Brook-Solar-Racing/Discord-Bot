from databaseManager import initializeNewUserData, initializePreDefinedUserData

example_data = False

if example_data:
    initializePreDefinedUserData(405918053226774538)
else:
    initializeNewUserData(405918053226774538)