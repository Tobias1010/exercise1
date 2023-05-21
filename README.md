# Prerequisite
python 3.9+

OS tested:
 * Windows

# Installation
Open a terminal and navigate to your working directory.


Clone repository:
```commandline
git clone https://github.com/Tobias1010/exercise1.git
```

Create virtual env and install dependencies:
```commandline
conda create -n my_venv python
conda activate my_venv
pip install -r requirements.txt
```

Initialise the app:
```commandline
uvicorn main:app --reload
```


# Framework
FastAPI + Strawberry + SQLlite database

Note that for simplicity the database has been pushed to github as well. 
you can delete the file (./db/people.db) and regenerate it from scratch by running the below script from the commandline:
```commandline
python source\my_database.py
```

# Queries
## Query all people
```commandline
query {
  people {
    email
    name
    address {
      number
      street
      city
      state
    }
  }
}
```

## Query one single person
```commandline
query {
  person (email: "profile1@gmail.com") {
    email
    name
    address {
      number
      street
      city
      state
    }
  }
}
```

# Mutations
## Add person (handling errors included)
### success
```commandline
mutation {
  addPerson(name: "Profile3", email: "profile3@gmail.com", street: "address3", number:3, city: "Brisbane", state: "Queensland") {
    __typename
    ... on Person {
         email
    		name
    		address {
          number
          street
          city
          state
    		}
    }
    ... on PersonError {
      name
      email
      message
    }
  }
}
```

### Error state outside available options
```commandline
mutation {
  addPerson(name: "Profile4", email: "profile4@gmail.com", street: "address4", number:4, city: "Genova", state: "Italy") {
    __typename
    ... on Person {
         email
    		name
    		address {
          number
          street
          city
          state
    		}
    }
    ... on PersonError {
      name
      email
      message
    }
  }
}
```

### Error email already exists
```commandline
mutation {
  addPerson(name: "Profile4", email: "profile3@gmail.com", street: "address4", number:4, city: "Perth", state: "Western Australia") {
    __typename
    ... on Person {
         email
    		name
    		address {
          number
          street
          city
          state
    		}
    }
    ... on PersonError {
      name
      email
      message
    }
  }
}
```
## Remove person
```commandline
mutation {
  removePerson(email: "profile2@gmail.com") {
    email
    name
    address {
      number
      street
      city
      state
    }
  }
}
```
