"""
Master configuration for all CSIT semesters
Edit this file to add/modify subjects, chapters, and syllabus
"""

COURSE_STRUCTURE = {
    1: {
        "name": "First Semester",
        "subjects": {
            "IIT": {
                "full_name": "Introduction to Information Technology",
                "chapters": [
                    "Unit 1: Introduction to Computer",
                    "Unit 2: The Computer System Hardware",
                    "Unit 3: Computer Memory",
                    "Unit 4: Input and Output Devices",
                    "Unit 5: Data Representation",
                    "Unit 6: Computer Software",
                    "Unit 7: Data Communication and Computer Network",
                    "Unit 8: The Internet and Internet Services",
                    "Unit 9: Fundamentals of Database",
                    "Unit 10: Multimedia",
                    "Unit 11: Computer Security"
                ]
            },
            "C_Programming": {
                "full_name": "C Programming",
                "chapters": [
                    "Unit 1: Problem Solving with Computer",
                    "Unit 2: Elements of C",
                    "Unit 3: Input and Output",
                    "Unit 4: Operators and Expression",
                    "Unit 5: Control Statement",
                    "Unit 6: Arrays",
                    "Unit 7: Functions",
                    "Unit 8: Structure and Union",
                    "Unit 9: Pointers",
                    "Unit 10: File Handling in C",
                    "Unit 11: Introduction to Graphics"
                ]
            },
            "DL": {
                "full_name": "Digital Logic",
                "chapters": [
                    "Unit 1: Binary Systems",
                    "Unit 2: Boolean algebra and Logic Gates",
                    "Unit 3: Simplification of Boolean Functions",
                    "Unit 4: Combinational Logic",
                    "Unit 5: Combinational Logic with MSI and LSI",
                    "Unit 6: Synchronous and Asynchronous Sequential Logic",
                    "Unit 7: Registers and Counters"
                ]
            },
            "Maths_I": {
                "full_name": "Mathematics I",
                "chapters": [
                    "Unit 1: Function of One Variable",
                    "Unit 2: Limits and Continuity",
                    "Unit 3: Derivatives",
                    "Unit 4: Applications of Derivatives",
                    "Unit 5: Antiderivatives",
                    "Unit 6: Applications of Antiderivatives",
                    "Unit 7: Ordinary Differential Equations",
                    "Unit 8: Infinite Sequence and Series",
                    "Unit 9: Plane and Space Vectors",
                    "Unit 10: Partial Derivatives and Multiple Integrals"
                ]
            },
            "Physics": {
                "full_name": "Physics",
                "chapters": [
                    "Unit 1: Rotational Dynamics and Oscillatory Motion",
                    "Unit 2: Electric and Magnetic Field",
                    "Unit 3: Fundamentals of Atomic Theory",
                    "Unit 4: Methods of Quantum Mechanics",
                    "Unit 5: Fundamentals of Solid State Physics",
                    "Unit 6: Semiconductor and Semiconductor devices",
                    "Unit 7: Universal Gates and Physics of Integrated Circuits"
                ]
            }
        }
    },
    2: {
        "name": "Second Semester",
        "subjects": {
            "Discrete_Structures": {
                "full_name": "Discrete Structures",
                "chapters": [
                    "Unit 1: Basic Discrete Structures",
                    "Unit 2: Integers and Matrices",
                    "Unit 3: Logic and Proof Methods",
                    "Unit 4: Induction and Recursion",
                    "Unit 5: Counting and Discrete Probability",
                    "Unit 6: Relations and Graphs"
                ]
            },
            "OOP": {
                "full_name": "Object Oriented Programming",
                "chapters": [
                    "Unit 1: Introduction to Object Oriented Programming",
                    "Unit 2: Basics of C++ programming",
                    "Unit 3: Classes & Objects",
                    "Unit 4: Operator Overloading",
                    "Unit 5: Inheritance",
                    "Unit 6: Virtual Function, Polymorphism, and miscellaneous C++ Features",
                    "Unit 7: Function Templates and Exception Handling",
                    "Unit 8: File handling"
                ]
            },
            "Microprocessor": {
                "full_name": "Microprocessor",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Basic Architecture",
                    "Unit 3: Instruction Cycle",
                    "Unit 4: Assembly Language Programming",
                    "Unit 5: Basic I/O, Memory R/W and Interrupt Operations",
                    "Unit 6: Input/ Output Interfaces",
                    "Unit 7: Advanced Microprocessors"
                ]
            },
            "Maths_II": {
                "full_name": "Mathematics II",
                "chapters": [
                    "Unit 1: Linear Equations in Linear Algebra",
                    "Unit 2: Transformation",
                    "Unit 3: Matrix Algebra",
                    "Unit 4: Determinants",
                    "Unit 5: Vector Spaces",
                    "Unit 6: Vector Space Continued",
                    "Unit 7: Eigenvalues and Eigen Vectors",
                    "Unit 8: Orthogonality and Least Squares",
                    "Unit 9: Groups and Subgroups",
                    "Unit 10: Rings and Fields"
                ]
            },
            "Statistics_I": {
                "full_name": "Statistics I",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Descriptive Statistics",
                    "Unit 3: Introduction to Probability",
                    "Unit 4: Sampling",
                    "Unit 5: Random Variables and Mathematical Expectation",
                    "Unit 6: Probability Distributions",
                    "Unit 7: Correlation and Linear Regression"
                ]
            }
        }
    },
    3: {
        "name": "Third Semester",
        "subjects": {
            "DSA": {
                "full_name": "Data Structures and Algorithms",
                "chapters": [
                    "Unit 1: Introduction to Data Structures & Algorithms",
                    "Unit 2: Stack",
                    "Unit 3: Queue",
                    "Unit 4: Recursion",
                    "Unit 5: Lists",
                    "Unit 6: Sorting",
                    "Unit 7: Searching and Hashing",
                    "Unit 8: Trees and Graphs"
                ]
            },
            "Numerical_Method": {
                "full_name": "Numerical Method",
                "chapters": [
                    "Unit 1: Solution of Nonlinear Equations",
                    "Unit 2: Interpolation and Regression",
                    "Unit 3: Numerical Differentiation and Integration",
                    "Unit 4: Solving System of Linear Equations",
                    "Unit 5: Solution of Ordinary Differential Equations",
                    "Unit 6: Solution of Partial Differential Equations"
                ]
            },
            "Computer_Architecture": {
                "full_name": "Computer Architecture",
                "chapters": [
                    "Unit 1: Data Representation",
                    "Unit 2: Register Transfer and Microoperations",
                    "Unit 3: Basic Computer Organization and Design",
                    "Unit 4: Microprogrammed Control",
                    "Unit 5: Central Processing Unit",
                    "Unit 6: Pipelining",
                    "Unit 7: Computer Arithmetic",
                    "Unit 8: Input Output Organization",
                    "Unit 9: Memory Organization"
                ]
            },
            "Computer_Graphics": {
                "full_name": "Computer Graphics",
                "chapters": [
                    "Unit 1: Introduction of Computer Graphics",
                    "Unit 2: Scan Conversion Algorithm",
                    "Unit 3: Two-Dimensional Geometric Transformations",
                    "Unit 4: Three-Dimensional Geometric Transformation",
                    "Unit 5: 3D Objects Representation",
                    "Unit 6: Solid Modeling",
                    "Unit 7: Visible Surface Detections",
                    "Unit 8: Illumination Models and Surface Rendering Techniques",
                    "Unit 9: Introduction to Virtual Reality",
                    "Unit 10: Introduction to OpenGL"
                ]
            },
            "Statistics_II": {
                "full_name": "Statistics II",
                "chapters": [
                    "Unit 1: Sampling Distribution and Estimation",
                    "Unit 2: Testing of hypothesis",
                    "Unit 3: Non parametric test",
                    "Unit 4: Multiple correlation and regression",
                    "Unit 5: Design of experiment",
                    "Unit 6: Stochastic Process"
                ]
            }
        }
    },
    4: {
        "name": "Fourth Semester",
        "subjects": {
            "TOC": {
                "full_name": "Theory of Computation",
                "chapters": [
                    "Unit I: Basic Foundations",
                    "Unit II: Introduction to Finite Automata",
                    "Unit III: Regular Expressions",
                    "Unit IV: Context Free Grammar",
                    "Unit V: Push Down Automata",
                    "Unit VI: Turing Machines",
                    "Unit VII: Undecidability and Intractability"
                ]
            },
            "Computer_Networks": {
                "full_name": "Computer Networks",
                "chapters": [
                    "Unit 1: Introduction to Computer Network",
                    "Unit 2: Physical Layer and Network Media",
                    "Unit 3: Data Link Layer",
                    "Unit 4: Network Layer",
                    "Unit 5: Transport Layer",
                    "Unit 6: Application Layer",
                    "Unit 7: Multimedia & Future Networking"
                ]
            },
            "Operating_Systems": {
                "full_name": "Operating Systems",
                "chapters": [
                    "Unit 1: Operating System Overview",
                    "Unit 2: Process Management",
                    "Unit 3: Process Deadlocks",
                    "Unit 4: Memory Management",
                    "Unit 5: File Management",
                    "Unit 6: Device Management",
                    "Unit 7: Linux Case Study"
                ]
            },
            "DBMS": {
                "full_name": "Database Management System",
                "chapters": [
                    "Unit 1: Database and Database Users",
                    "Unit 2: Database System – Concepts and Architecture",
                    "Unit 3: Data Modeling Using the Entity-Relational Model",
                    "Unit 4: The Relational Data Model and Relational Database Constraints",
                    "Unit 5: The Relational Algebra and Relational Calculus",
                    "Unit 6: SQL",
                    "Unit 7: Relational Database Design",
                    "Unit 8: Introduction to Transaction Processing Concepts and Theory",
                    "Unit 9: Concurrency Control Techniques",
                    "Unit 10: Database Recovery Techniques"
                ]
            },
            "AI": {
                "full_name": "Artificial Intelligence",
                "chapters": [
                    "Unit I: Introduction",
                    "Unit II: Intelligent Agents",
                    "Unit III: Problem Solving by Searching",
                    "Unit IV: Knowledge Representation",
                    "Unit V: Machine Learning",
                    "Unit VI: Applications of AI"
                ]
            }
        }
    },
    5: {
        "name": "Fifth Semester",
        "subjects": {
            "DAA": {
                "full_name": "Design and Analysis of Algorithms",
                "chapters": [
                    "Unit 1: Foundation of Algorithm Analysis",
                    "Unit 2: Iterative Algorithms",
                    "Unit 3: Divide and Conquer Algorithms",
                    "Unit 4: Greedy Algorithms",
                    "Unit 5: Dynamic Programming",
                    "Unit 6: Backtracking",
                    "Unit 7: Number Theoretic Algorithms",
                    "Unit 8: NP Completeness"
                ]
            },
            "SAD": {
                "full_name": "System Analysis and Design",
                "chapters": [
                    "Unit 1: Foundations for Systems Development",
                    "Unit 2: Planning",
                    "Unit 3: Analysis",
                    "Unit 4: Design",
                    "Unit 5: Implementation and Maintenance",
                    "Unit 6: Introduction to Object-Oriented Development"
                ]
            },
            "Cryptography": {
                "full_name": "Cryptography",
                "chapters": [
                    "Unit I: Introduction and Classical Ciphers",
                    "Unit II: Symmetric Ciphers",
                    "Unit III: Asymmetric Ciphers",
                    "Unit IV: Cryptographic Hash Functions and Digital Signatures",
                    "Unit V: Authentication",
                    "Unit VI: Network Security and Public Key Infrastructure",
                    "Unit VII: Malicious Logic"
                ]
            },
            "Simulation_and_Modeling": {
                "full_name": "Simulation and Modeling",
                "chapters": [
                    "Unit 1: Introduction to Simulation",
                    "Unit 2: Simulation of Continuous and Discrete System",
                    "Unit 3: Queuing System",
                    "Unit 4: Markov Chains",
                    "Unit 5: Random Numbers",
                    "Unit 6: Verification and Validation",
                    "Unit 7: Analysis of Simulation Output",
                    "Unit 8: Simulation of Computer Systems"
                ]
            },
            "Web_Technology": {
                "full_name": "Web Technology",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Hyper Text Markup Language",
                    "Unit 3: Cascading Style Sheets",
                    "Unit 4: Client Side Scripting with JavaScript",
                    "Unit 5: AJAX and XML",
                    "Unit 6: Server Side Scripting using PHP"
                ]
            },
            "Multimedia_Computing": {
                "full_name": "Multimedia Computing (Elective I)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Sound /Audio System",
                    "Unit 3: Images and Graphics",
                    "Unit 4: Video and Animation",
                    "Unit 5: Data Compression",
                    "Unit 7: User Interfaces",
                    "Unit 8: Abstractions for programming",
                    "Unit 9: Multimedia Application"
                ]
            },
            "Wireless_Networking": {
                "full_name": "Wireless Networking (Elective I)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Wireless Channel Characterization",
                    "Unit 3: Wireless Communication Techniques",
                    "Unit 4: Fundamental of Cellular Communications",
                    "Unit 5: Mobility Management in Wireless Networks",
                    "Unit 6: Overview of Mobile Network and Transport Layer",
                    "Unit 7: Advances in Wireless Networking"
                ]
            },
            "Image_Processing": {
                "full_name": "Image Processing (Elective I)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Image Enhancement and Filter in Spatial Domain",
                    "Unit 3: Image Enhancement in the Frequency Domain",
                    "Unit 4: Image Restoration and Compression",
                    "Unit 5: Introduction to Morphological Image Processing",
                    "Unit 6: Image Segmentation",
                    "Unit 7: Representations, Description and Recognition"
                ]
            },
            "Knowledge_Management": {
                "full_name": "Knowledge Management (Elective I)",
                "chapters": [
                    "Unit 1",
                    "Unit 2",
                    "Unit 3",
                    "Unit 4",
                    "Unit 5"
                ]
            },
            "Society_and_Ethics_in_IT": {
                "full_name": "Society and Ethics in Information Technology (Elective I)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Social and cultural change",
                    "Unit 3: Understanding development",
                    "Unit 4: Process of transformation",
                    "Unit 5: Ethics and Ethical Analysis",
                    "Unit 6: Intellectual Property Rights and Computer Technology",
                    "Unit 7: Social Context of Computing",
                    "Unit 8: Software Issues",
                    "Unit 9: New Frontiers for Computer Ethics"
                ]
            },
            "Microprocessor_Based_Design": {
                "full_name": "Microprocessor Based Design (Elective I)",
                "chapters": [
                    "Unit 1: Introduction to Microcontroller",
                    "Unit 2: Sensors and Actuators",
                    "Unit 3: Bus and Communication Technology",
                    "Unit 4: Introduction to 8051 Microcontroller and Programming",
                    "Unit 5: Electromagnetic Interference and Compatibility"
                ]
            }
        }
    },
    6: {
        "name": "Sixth Semester",
        "subjects": {
            "Software_Engineering": {
                "full_name": "Software Engineering",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Software Processes",
                    "Unit 3: Agile Software Development",
                    "Unit 4: Requirements Engineering",
                    "Unit 5: System Modeling",
                    "Unit 6: Architectural Design",
                    "Unit 7: Design and Implementation",
                    "Unit 8: Software Testing",
                    "Unit 9: Software Evolution",
                    "Unit 10: Software Management"
                ]
            },
            "Compiler_Design": {
                "full_name": "Compiler Design and Construction",
                "chapters": [
                    "Unit 1",
                    "Unit 2",
                    "Unit 3",
                    "Unit 4"
                ]
            },
            "E_Governance": {
                "full_name": "E-Governance",
                "chapters": [
                    "Unit 1: Introduction to E-Government and E-Governance",
                    "Unit 2: Models of E-Governance",
                    "Unit 3: E-Government Infrastructure Development",
                    "Unit 4: Security for e-Government",
                    "Unit 5: Applications of Data Warehousing and Data Mining in Government",
                    "Unit 6: Case Studies"
                ]
            },
            "NET_Centric_Computing": {
                "full_name": "NET Centric Computing",
                "chapters": [
                    "Unit 1: Language Preliminaries",
                    "Unit 2: Introduction to ASP.NET",
                    "Unit 3: HTTP and ASP.NET Core",
                    "Unit 4: Creating ASP.NET core MVC applications",
                    "Unit 5: Working with Database",
                    "Unit 6: State Management on ASP.NET Core Application",
                    "Unit 7: Client-side Development in ASP.NET Core",
                    "Unit 8: Securing in ASP.NET Core Application",
                    "Unit 9: Hosting and Deploying ASP.NET Core Application"
                ]
            },
            "Technical_Writing": {
                "full_name": "Technical Writing",
                "chapters": [
                    "Unit 1: What Is Technical Writing",
                    "Unit 2: Audience and Purpose",
                    "Unit 3: Writing Process",
                    "Unit 4: Brief Correspondence",
                    "Unit 5: Document Design and Graphics",
                    "Unit 6: Writing for the Web",
                    "Unit 7: Information Reports",
                    "Unit 8: Employment Communication",
                    "Unit 9: Presentations",
                    "Unit 10: Recommendation Reports",
                    "Unit 11: Proposals",
                    "Unit 12: Ethics in the Workplace"
                ]
            },
            "Applied_Logic": {
                "full_name": "Applied Logic (Elective II)",
                "chapters": [
                    "Unit 1: Argument Analysis",
                    "Unit 2: Categorical Propositions and Syllogisms",
                    "Unit 3: Symbolic Logic",
                    "Unit 4: Quantification Theory",
                    "Unit 5: Fallacies",
                    "Unit 6: Analogical and Casual Reasoning"
                ]
            },
            "E_Commerce": {
                "full_name": "E-Commerce (Elective II)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: E-commerce Business Model",
                    "Unit 3: Electronic Payment System",
                    "Unit 4: Building E-commerce System",
                    "Unit 5: Security in E-Commerce",
                    "Unit 6: Digital Marketing",
                    "Unit 7: Optimizing E-commerce Systems"
                ]
            },
            "Automation_and_Robotics": {
                "full_name": "Automation and Robotics (Elective II)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Power Sources and Sensors",
                    "Unit 3: Manipulators, Actuators, and Grippers",
                    "Unit 4: Kinematics and Path Planning",
                    "Unit 5: Process Control",
                    "Unit 6: Case Studies"
                ]
            },
            "Neural_Networks": {
                "full_name": "Neural Networks (Elective II)",
                "chapters": [
                    "Unit 1: Introduction to Neural Network",
                    "Unit 2: Rosenblatt’s Perceptron",
                    "Unit 3: Model Building through Regression",
                    "Unit 4: The Least-Mean-Square Algorithm",
                    "Unit 5: Multilayer Perceptron",
                    "Unit 6: Kernel Methods and Radial-Basis Function Networks",
                    "Unit 7: Self-Organizing Maps",
                    "Unit 8: Dynamic Driven Recurrent Networks"
                ]
            },
            "Computer_Hardware_Design": {
                "full_name": "Computer Hardware Design (Elective II)",
                "chapters": [
                    "Unit 1: Computer Abstractions and Technology",
                    "Unit 2: Instructions: Language of the Computer",
                    "Unit 3: Arithmetic for Computers",
                    "Unit 4: The Processor",
                    "Unit 5: Large and Fast: Exploiting Memory Hierarchy",
                    "Unit 6: Storage and Other I/O Topics",
                    "Unit 7: Multicores, Multiprocessors, and Clusters"
                ]
            },
            "Cognitive_Science": {
                "full_name": "Cognitive Science (Elective II)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Precursors of Cognitive Science",
                    "Unit 3: Psycological Perspective of Cognition",
                    "Unit 4: Physical Symbol System and Language of Thought",
                    "Unit 5: Cognitive System",
                    "Unit 6: Brain Mapping",
                    "Unit 7: Mind Reading",
                    "Unit 8: Neural Networks and Distributed Information Processing"
                ]
            }
        }
    },
    7: {
        "name": "Seventh Semester",
        "subjects": {
            "Advanced_Java_Programming": {
                "full_name": "Advanced Java Programming",
                "chapters": [
                    "Unit 1: Programming in Java",
                    "Unit 2: User Interface Components with Swing",
                    "Unit 3: Event Handling",
                    "Unit 4: Database Connectivity",
                    "Unit 5: Network Programming",
                    "Unit 6: GUI with JavaFX",
                    "Unit 7: Servlets and Java Server pages",
                    "Unit 8: RMI and CORBA"
                ]
            },
            "Data_Warehousing_and_Data_Mining": {
                "full_name": "Data Warehousing and Data Mining",
                "chapters": [
                    "Unit 1: Introduction to Data Warehousing",
                    "Unit 2: Introduction to Data Mining",
                    "Unit 3: Data Preprocessing",
                    "Unit 4: Data Cube Technology",
                    "Unit 5: Mining Frequent Patterns",
                    "Unit 6: Classification and Prediction",
                    "Unit 7: Cluster Analysis",
                    "Unit 8: Graph Mining and Social Network Analysis",
                    "Unit 9: Mining Spatial, Multimedia, Text and Web Data"
                ]
            },
            "Principles_of_Management": {
                "full_name": "Principles of Management",
                "chapters": [
                    "Unit 1: The Nature of Organizations",
                    "Unit 2: Introduction to Management",
                    "Unit 3: Evolution of Management Thought",
                    "Unit 4: Environmental Context of Management",
                    "Unit 5: Planning and Decision Making",
                    "Unit 6: Organizing Function",
                    "Unit 7: Leadership & Conflict",
                    "Unit 8: Motivation",
                    "Unit 9: Communication",
                    "Unit 10: Control and Quality Management",
                    "Unit 11: Global Context of Management",
                    "Unit 12: Management Trends and Scenario in Nepal"
                ]
            },
            "Project_Work": {
                "full_name": "Project Work",
                "chapters": [
                    "Nature of Project",
                    "Phases of Project",
                    "Provision of Supervision",
                    "Evaluation Scheme",
                    "Roles and Responsibilities",
                    "Report Contents"
                ]
            },
            "Information_Retrieval": {
                "full_name": "Information Retrieval (Elective III)",
                "chapters": [
                    "Unit 1: Introduction to IR and Web Search",
                    "Unit 2: Text properties, operations and preprocessing",
                    "Unit 3: Basic IR Models",
                    "Unit 4: Evaluation of IR",
                    "Unit 5: Query Operations and Languages",
                    "Unit 6: Web Search",
                    "Unit 7: Text Categorization",
                    "Unit 8: Text Clustering",
                    "Unit 9: Recommender System",
                    "Unit 10: Question Answering",
                    "Unit 11: Advanced IR Models"
                ]
            },
            "Database_Administration": {
                "full_name": "Database Administration (Elective III)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Tablespace and Storage management",
                    "Unit 3: Managing Database Objects",
                    "Unit 4: Database Backup, Restore, and Recovery",
                    "Unit 5: Database Security and Auditing",
                    "Unit 6: Multitenant Database Architecture",
                    "Unit 7: Database Tuning"
                ]
            },
            "Software_Project_Management": {
                "full_name": "Software Project Management (Elective III)",
                "chapters": [
                    "Unit 1: Introduction to Software Project Management",
                    "Unit 2: Project Analysis",
                    "Unit 3: Activity Planning and Scheduling",
                    "Unit 4: Risk Management",
                    "Unit 5: Resource Allocation",
                    "Unit 6: Monitoring and Control",
                    "Unit 7: Managing Contracts and people",
                    "Unit 8: Software quality assurance and testing",
                    "Unit 9: Software Configuration Management"
                ]
            },
            "Network_Security": {
                "full_name": "Network Security (Elective III)",
                "chapters": [
                    "Unit 1: Computer Network Security Fundamentals",
                    "Unit 2: User Authentication",
                    "Unit 3: Transport Level Security",
                    "Unit 4: Wireless Network Security",
                    "Unit 5: Electronic Mail Security",
                    "Unit 6: IP Security",
                    "Unit 7: Network Endpoint Security",
                    "Unit 8: Cloud and Internet of Things (IOT) Security"
                ]
            },
            "Digital_System_Design": {
                "full_name": "Digital System Design (Elective III)",
                "chapters": [
                    "Unit 1: Introduction of logic design",
                    "Unit 2: Review of Boolean Algebra and Combinational Logic",
                    "Unit 3: Combinational Network Design",
                    "Unit 4: Quine- Mc Cluskey Method",
                    "Unit 5: Sequential Networks",
                    "Unit 6: Sequential Networks as Finite State Machines",
                    "Unit 7: Field Programmable Gate Arrays (FPGA)",
                    "Unit 8: Testing and Verification"
                ]
            },
            "International_Marketing": {
                "full_name": "International Marketing (Elective III)",
                "chapters": [
                    "Unit 1. Introduction",
                    "Unit 2. International Marketing Environment",
                    "Unit 3: International Marketing Research Global Marketing Information System",
                    "Unit 4: International Marketing Management",
                    "Unit 5: Nepal’s International Trade"
                ]
            }
        }
    },
    8: {
        "name": "Eighth Semester",
        "subjects": {
            "Advanced_Database": {
                "full_name": "Advanced Database",
                "chapters": [
                    "Unit 1: Enhanced Entity Relationship Model and Relational Model",
                    "Unit 2: Object and Object Relational Databases",
                    "Unit 3: Query Processing and Optimization",
                    "Unit 4: Distributed Databases, NOSQL Systems, and BigData",
                    "Unit 5: Advanced Database Models, Systems, and Applications"
                ]
            },
            "Internship": {
                "full_name": "Internship",
                "chapters": [
                    "Nature of Internship",
                    "Phases of Internship",
                    "Provision of Supervision",
                    "Provision of Mentorship",
                    "Evaluation Scheme",
                    "Report Contents"
                ]
            },
            "Advanced_Networking_with_IPv6": {
                "full_name": "Advanced Networking with IPv6 (Elective IV/V)",
                "chapters": [
                    "Unit 1: Introduction to Networking",
                    "Unit 2: IP Next Generation",
                    "Unit 3: ICMPv6 and Neighbor Discovery",
                    "Unit 4: Security and Quality of Service in IPv6",
                    "Unit 5: IPv6 Routing",
                    "Unit 6: IPv4/IPv6 Transition Mechanisms",
                    "Unit 7: Future networking"
                ]
            },
            "Distributed_Networking": {
                "full_name": "Distributed Networking (Elective IV/V)",
                "chapters": [
                    "Unit 1 Overview",
                    "Unit 2 Client Server Model",
                    "Unit 3 Communication Paradigm",
                    "Unit 4 Internetworking",
                    "Unit 5 Interprocess communication using message passing",
                    "Unit 6 Reliability and Replication Techniques",
                    "Unit 7 Security",
                    "Unit 8 Current Developments in Distributed Network System"
                ]
            },
            "Game_Technology": {
                "full_name": "Game Technology (Elective IV/V)",
                "chapters": [
                    "Unit 1: Game Design Basics",
                    "Unit 2: Designing a Game",
                    "Unit 3: Working as a Game Designer"
                ]
            },
            "Distributed_and_Object_Oriented_Database": {
                "full_name": "Distributed and Object Oriented Database (Elective IV/V)",
                "chapters": [
                    "Unit 1: Introduction to Distributed Database",
                    "Unit 2: Distributed Database Design and Access Control",
                    "Unit 3: Query Processing, Decomposition, and Localization",
                    "Unit 4: Distributed Concurrency Control",
                    "Unit 5: Object Oriented Database Concepts",
                    "Unit 6: OODBMS Languages and Design"
                ]
            },
            "Introduction_to_Cloud_Computing": {
                "full_name": "Introduction to Cloud Computing (Elective IV/V)",
                "chapters": [
                    "Unit 1: Introduction to Cloud Computing",
                    "Unit 2: Cloud Computing Architecture",
                    "Unit 3: Cloud Virtualization technology",
                    "Unit 4: Cloud Programming Models",
                    "Unit 5: Cloud security",
                    "Unit 6: Cloud Platforms and Applications"
                ]
            },
            "Geographical_Information_System": {
                "full_name": "Geographical Information System (Elective IV/V)",
                "chapters": [
                    "Unit 1: Introduction to Geographic Information System (GIS)",
                    "Unit 2: Digital Mapping Concepts and Visualization",
                    "Unit 3: Spatial Data Structure and Database Design",
                    "Unit 4: Data Acquisition, Data Quality and Management",
                    "Unit 5: Spatial Analysis",
                    "Unit 6: Introduction to Spatial Data Infrastructure",
                    "Unit 7: Open GIS"
                ]
            },
            "Decision_Support_System_and_Expert_System": {
                "full_name": "Decision Support System and Expert System (Elective IV/V)",
                "chapters": [
                    "Unit 1: Business Decision Making",
                    "Unit 2: Designing, Developing, and Evaluating DSS Systems",
                    "Unit 3: Building DSS Systems",
                    "Unit 4: Expert Systems",
                    "Unit 5: Fuzzy Expert Systems"
                ]
            },
            "Mobile_Application_Development": {
                "full_name": "Mobile Application Development (Elective IV/V)",
                "chapters": [
                    "Unit 1: Introduction to Mobile Computing",
                    "Unit 2: Architecture, Design and Mobile Development Frameworks",
                    "Unit 3: User Interfaces",
                    "Unit 4: Testing and Publishing Apps",
                    "Unit 5: Mobile Agent and Peer-to-Peer Architectures for Mobile Applications",
                    "Unit 6: Wireless Connectivity and Mobile Applications",
                    "Unit 7: Synchronization and Replication of Mobile Data",
                    "Unit 8: Location and Sensing",
                    "Unit 9: Active Transactions"
                ]
            },
            "Real_Time_Systems": {
                "full_name": "Real Time Systems (Elective IV/V)",
                "chapters": [
                    "Unit 1: Introduction",
                    "Unit 2: Reference Model of Real Time System",
                    "Unit 3: Periodic Task Scheduling",
                    "Unit 4: Aperiodic Task Scheduling",
                    "Unit 5: Real-Time Memory Management",
                    "Unit 6: Resources and Resource Access Control",
                    "Unit 7: Performance Analysis and Optimization of Real-Time Systems",
                    "Unit 8: Real Time Communication"
                ]
            },
            "Network_and_System_Administration": {
                "full_name": "Network and System Administration (Elective IV/V)",
                "chapters": [
                    "Unit 1: Networking Overview",
                    "Unit 2: Server Administration Basics",
                    "Unit 3: Network Configuration Basics",
                    "Unit 4: Dynamic Host Configuration Protocol (DHCP)",
                    "Unit 5: Name Server and Configuration",
                    "Unit 6: Web and Proxy Server Configuration",
                    "Unit 7: FTP, File, and Print Server",
                    "Unit 8: Mail Server basics"
                ]
            },
            "Embedded_Systems_Programming": {
                "full_name": "Embedded Systems Programming (Elective IV/V)",
                "chapters": [
                    "Unit 1: ARM Embedded System",
                    "Unit 2: ARM Processor Fundamentals",
                    "Unit 3: Introduction to ARM Instruction Set",
                    "Unit 4: Thumb Instruction Set",
                    "Unit 5: Efficient C Programming for ARM",
                    "Unit 6: Writing and Optimizing ARM Assembly Code",
                    "Unit 7: Firmware and Embedded OS"
                ]
            },
            "International_Business_Management": {
                "full_name": "International Business Management (Elective IV/V)",
                "chapters": [
                    "Unit 1: Globalization and International Business",
                    "Unit 2: Global Economy and Regional Economy",
                    "Unit 3: National Differences in Socio-cultural Environment",
                    "Unit 4: National Differences in Political Environment",
                    "Unit 5: National Differences in Economic Environment",
                    "Unit 6: International Financial Environment",
                    "Unit 7: Strategies for IB",
                    "Unit 8: Functional Management and Operation of IB"
                ]
            }
        }
    }
}

# Helper function to get subject chapters
def get_chapters(semester: int, subject_code: str):
    return COURSE_STRUCTURE.get(semester, {}).get("subjects", {}).get(subject_code, {}).get("chapters", [])

# Helper function to get all subjects for a semester
def get_subjects(semester: int):
    return COURSE_STRUCTURE.get(semester, {}).get("subjects", {})