# udp_principles.py — The 7 Universal Design Principles
# ======================================================
# TODO: Fill in the full list of 7 principles.
# Each principle should have:
#   - "id": int (1-7)
#   - "name": string
#   - "description": what the principle means
#   - "bridge_criteria": list of strings — what to look for on a bridge
#
# The first one is done for you as an example. Do the remaining 6!
# Think about what each principle means specifically for BRIDGE accessibility.

UDP_PRINCIPLES = [
    {
        "id": 1,
        "name": "Equitable Use",
        "description": "The design is useful and marketable to people with diverse abilities.",
        "bridge_criteria": [
            "Ramps available as alternatives to stairs",
            "Same path of travel available to all users",
            "No segregation of users by ability",
        ]
    },
    {
        "id": 2,
        "name": "Flexibility in Use",
        "description": "The design encompasses many different preferences and methods",
        "bridge_criteria": [
            "Does the bridge offer different ways of access? ",
            "Does the bridge allow crossing on both sides?",
            "Does the bridge accomodate differnt modes of transportation?"
        ]
    },
    {
        "id": 3,
        "name": "Simple and Intuitive Use",
        "description": "Use of the design is easy to understand, regardless of the user's experience, knowledge, language skills, or current concentration level",
        "bridge_criteria": [
            "Are the entrances to the bridge clearly indicated?",
            "Does navigating across the bridge look straightforward from the view of all types of transportation types?",
            "Does the bridge use universal or multilingual signage to indicate the correct pathway?",
            "Are the path markings clear and easy to understand for all types of transportation?",
        ]
    },
    {
        "id": 4,
        "name": "Perceptible Information",
        "description": "The design communicates necessary information effectively to the user, regardless of ambient conditions or the user's sensory abilities.", 
        "bridge_criteria":  [
            "Are there sensory aids for people with sensory limitations like blindess and deafness?",
            "Are the signs designed in a way that is readable to people with different levels of vision?",
            "Are the signs designed so that transportation of all types can see them?"
            "Are there tactical pavings, textured surfaces at transitions, and edge markings that communicate to all types of transportations and people?",
            "Does the bridge have lighting at night for people to perceive the path and potential hazards?"
        ]
    },
    {
        "id":5,
        "name": "Tolerance for Error",
        "description": "The design minimizes hazards and the adverse consequences of accidental or unintended actions.",
        "bridge_criteria" : [
            "Are there safety railings, barriers, and general preventative components on this bridge?",
            "Are turns for transportations safe?",
            "Are there warning signs before terrain changes such as elevation and hazards?",
            "Are the ramps designed in a safe way that prevents accidents?"
        ]
    },
    {
        "id":6,
        "name": "Low Physical Effort",
        "description": "The design can be used efficiently and comfortably and with a minimum of fatigue.",
        "bridge_criteria" : [
            "Do the bridges have a gradual incline?",
            "Are there resting areas for pedestrians on longer bridges?",
            "Are there pull over areas for cars and vehicles?",
            "Are there any physically intensive actions that must be taken to access the bridge?"
        ]
    },
    {
        "id":7,
        "name": "Size and Space for Approach and Use",
        "description": "Appropriate size and space is provided for approach, reach, manipulation, and use regardless of user's body size, posture, or mobility.",
        "bridge_criteria" : [
            "Is it wide enough for pedestrians to comfortable pass through?",
            "Is there adequate clearance at the entrance?",
            "Is there seperation between different pedestrians and vehicles?",
        ]
    }
]
