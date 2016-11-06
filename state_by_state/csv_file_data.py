CANDIDATE_ID = 1
CANDIDATE_NAME = 2
CONTRIBUTOR_NAME = 3
CONTRIBUTOR_CITY = 4
CONTRIBUTOR_STATE = 5
CONTRIBUTOR_ZIP = 6
CONTRIBUTOR_EMPLOYER = 7
CONTRIBUTOR_OCCUPATION = 8
CONTRIBUTION_AMOUNT = 9
CONTRIBUTION_DATE = 10

DEMOCRATIC = 1
REPUBLICAN = 2
LIBERTARIAN = 3
OTHER = 4
GREEN = 5
INDEPENDENT = 6
UNKOWN = 7

# candidates
CANDIDATES = {
    # 2008
    'P80003478': REPUBLICAN, # Mike Huckabee
    'P80000748': REPUBLICAN, # Ron Paul
    'P80003395': REPUBLICAN, # Duncan Hunter
    'P80003338': DEMOCRATIC, # Barack Obama
    'P80003411': DEMOCRATIC, # Bill Richardson
    'P00003186': REPUBLICAN, # Fred Dalton Thompson
    'P00003392': DEMOCRATIC, # Hillary Clinton
    'P80002983': REPUBLICAN, # John Cox
    'P40002347': DEMOCRATIC, # John Edwards
    'P00003251': REPUBLICAN, # Rudolph Giuliani
    'P80003353': REPUBLICAN, # Mitt Romney
    'P80003288': REPUBLICAN, # Sam Brownback
    'P60003795': REPUBLICAN, # Tommy Thomson
    'P80003429': REPUBLICAN, # Thomas Tancredo
    'P80000722': DEMOCRATIC, # Joe Biden
    'P80003387': DEMOCRATIC, # Chris Dodd
    'P80002801': REPUBLICAN, # John Mccain
    'P40002545': DEMOCRATIC, # Dennis Kucinich
    'P60004751': LIBERTARIAN, # Mike Gravel
    'P80003379': REPUBLICAN, # James S III Gilmore
    # 2012
    'P80000748': REPUBLICAN, # Ron Paul
    #'P80003338': DEMOCRATIC, # Barack Obama
    'P60003654': REPUBLICAN, # Newt Gingrich
    'P20002978': REPUBLICAN, # Michele Bachmann
    'P20002523': OTHER, # Charles E. Buddy III Roemer
    'P20002556': REPUBLICAN, # Timothy Pawlenty
    'P20003281': REPUBLICAN, # Rick Perry
    'P00003608': REPUBLICAN, # Herman Cain
    #'P80003353': REPUBLICAN, # Mitt Romney
    'P20002721': REPUBLICAN, # Rick Santorum
    'P20003067': REPUBLICAN, # Jon Huntsman
    'P20002671': LIBERTARIAN, # Gary Earl Johnson
    'P20003984': GREEN, # Jill Stein
    'P20003109': REPUBLICAN, # Thaddeus G McCotter
    # 2016
    'P60007168': DEMOCRATIC, # Bernard Sanders
    'P60006111': REPUBLICAN, # Rafael Edward (Ted) Cruz
    'P60006046': REPUBLICAN, # Scott Walker
    'P60008059': REPUBLICAN, # Jeb Bush
    'P60006723': REPUBLICAN, # Marco Rubio
    'P80001571': REPUBLICAN, # Donald Trump
    'P60003670': REPUBLICAN, # John Kasich
    'P40003576': REPUBLICAN, # Rand Paul
    'P60007242': REPUBLICAN, # Carly Fiorina
    'P60005915': REPUBLICAN, # Benjamin S Sr Carson
    'P60022654': INDEPENDENT, # Evan McMullin
    'P60008521': REPUBLICAN, # Christopher Christie
    'P60007671': DEMOCRATIC, # Martin O'Malley
    'P60007697': REPUBLICAN, # Lindsey Graham
    'P60008398': REPUBLICAN, # Bobby Jindal
    'P60009685': DEMOCRATIC, # Lawrence Lessig
    'P60008885': UNKOWN, # James Web
    'P60007572': REPUBLICAN, # George Pataki
}

GENERAL_ELECTION_CANDIDATES = {
    '2008': {
        'P80003338': DEMOCRATIC, # Barack Obama
        'P80002801': REPUBLICAN, # John Mccain
    },
    '2012': {
        'P80003338': DEMOCRATIC, # Barack Obama
        'P80003353': REPUBLICAN # Mitt Romney
    },
    '2016': {
        'P00003392': DEMOCRATIC, # Hillary Clinton
        'P80001571': REPUBLICAN # Donald Trump
    }
}
