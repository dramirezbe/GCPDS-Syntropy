# Pseudocode Reference

Comprehensive pseudocode syntax and examples for educational and design purposes.

---

## 1. Basic Syntax

```pseudocode
ALGORITHM CalculateAverage

    DECLARE a AS INTEGER
    DECLARE b AS INTEGER
    DECLARE average AS FLOAT

    a ← 10
    b ← 20

    average ← (a + b) / 2

    PRINT average

END ALGORITHM
```

Common conventions:

| Symbol | Meaning |
|--------|---------|
| `←` | Assignment |
| `=` | Equality / comparison |

```pseudocode
x ← 10          // assign 10 to x
IF x = 10 THEN   // compare x with 10
```

---

## 2. Comments

```pseudocode
// Single-line comment

/*
   Multi-line comment
   explaining the algorithm
*/
```

---

## 3. Variables

```pseudocode
DECLARE name AS STRING
DECLARE age AS INTEGER
DECLARE temperature AS FLOAT
DECLARE enabled AS BOOLEAN
```

Assignment:

```pseudocode
name ← "Alice"
age ← 25
temperature ← 23.5
enabled ← TRUE
```

Type inference:

```pseudocode
name := "Alice"
count := 10
pi := 3.14159
```

---

## 4. Constants

```pseudocode
CONSTANT PI ← 3.14159265359
CONSTANT MAX_USERS ← 100
CONSTANT DEFAULT_TIMEOUT ← 30
```

With annotation:

```pseudocode
@const
MAX_USERS ← 100
```

---

## 5. Primitive Types

```pseudocode
INTEGER
FLOAT
DOUBLE
BOOLEAN
CHAR
STRING
BYTE
```

Example:

```pseudocode
DECLARE count AS INTEGER
DECLARE ratio AS DOUBLE
DECLARE active AS BOOLEAN
DECLARE initial AS CHAR
DECLARE message AS STRING
```

---

## 6. Type Conversion

```pseudocode
age ← 25
textAge ← TO_STRING(age)
number ← TO_INTEGER("123")
value ← TO_FLOAT("3.14")
```

Explicit syntax:

```pseudocode
converted ← CAST(value AS INTEGER)
```

---

## 7. Arithmetic Operators

| Operator | Meaning |
|----------|---------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `MOD` | Modulo |
| `^` | Power |

```pseudocode
remainder ← 17 MOD 5
power ← 2 ^ 8
```

---

## 8. Comparison Operators

| Operator | Meaning |
|----------|---------|
| `=` | Equal |
| `≠` | Not equal |
| `<` | Less than |
| `>` | Greater than |
| `≤` | Less than or equal |
| `≥` | Greater than or equal |

---

## 9. Logical Operators

```pseudocode
AND
OR
NOT
XOR
```

Example:

```pseudocode
IF age >= 18 AND active = TRUE THEN
    PRINT "User is active and adult"
END IF
```

---

## 10. Conditional — IF

```pseudocode
IF temperature > 30 THEN
    PRINT "Hot"
END IF
```

---

## 11. IF / ELSE

```pseudocode
IF score >= 60 THEN
    PRINT "Pass"
ELSE
    PRINT "Fail"
END IF
```

---

## 12. IF / ELSE IF / ELSE

```pseudocode
IF score >= 90 THEN
    grade ← "A"
ELSE IF score >= 80 THEN
    grade ← "B"
ELSE IF score >= 70 THEN
    grade ← "C"
ELSE IF score >= 60 THEN
    grade ← "D"
ELSE
    grade ← "F"
END IF
```

---

## 13. Nested Conditionals

```pseudocode
IF user IS NOT NULL THEN

    IF user.active = TRUE THEN

        IF user.age >= 18 THEN
            PRINT "Access granted"
        ELSE
            PRINT "Minor user"
        END IF

    ELSE
        PRINT "Account disabled"
    END IF

ELSE
    PRINT "No user"
END IF
```

---

## 14. SWITCH / CASE

```pseudocode
SWITCH command

    CASE "START":
        startSystem()

    CASE "STOP":
        stopSystem()

    CASE "RESET":
        resetSystem()

    DEFAULT:
        PRINT "Unknown command"

END SWITCH
```

---

## 15. Ternary Expression

```pseudocode
status ← IF temperature > 30 THEN "HOT" ELSE "NORMAL"
```

Equivalent:

```pseudocode
IF temperature > 30 THEN
    status ← "HOT"
ELSE
    status ← "NORMAL"
END IF
```

---

## 16. FOR Loop

```pseudocode
FOR i ← 0 TO 10 DO
    PRINT i
END FOR
```

With step:

```pseudocode
FOR i ← 0 TO 100 STEP 10 DO
    PRINT i
END FOR
```

---

## 17. WHILE Loop

```pseudocode
WHILE count < 10 DO
    PRINT count
    count ← count + 1
END WHILE
```

---

## 18. DO / WHILE

```pseudocode
DO
    input ← READ()
WHILE input ≠ "quit"
```

Guarantees at least one execution.

---

## 19. FOREACH

```pseudocode
FOR EACH user IN users DO
    PRINT user.name
END FOR
```

---

## 20. BREAK

```pseudocode
FOR i ← 1 TO 100 DO

    IF i = 50 THEN
        BREAK
    END IF

END FOR
```

---

## 21. CONTINUE

```pseudocode
FOR i ← 1 TO 10 DO

    IF i MOD 2 = 0 THEN
        CONTINUE
    END IF

    PRINT i

END FOR
```

---

## 22. Infinite Loop

```pseudocode
WHILE TRUE DO
    processData()
END WHILE
```

With exit condition:

```pseudocode
WHILE TRUE DO

    command ← READ_COMMAND()

    IF command = "EXIT" THEN
        BREAK
    END IF

    process(command)

END WHILE
```

---

## 23. Functions

```pseudocode
FUNCTION Add(a AS INTEGER, b AS INTEGER) RETURNS INTEGER
    RETURN a + b
END FUNCTION
```

Call:

```pseudocode
result ← Add(10, 20)
```

---

## 24. Procedure (No Return)

```pseudocode
PROCEDURE PrintMessage(message AS STRING)
    PRINT message
END PROCEDURE
```

Call:

```pseudocode
PrintMessage("Hello")
```

---

## 25. Function with Multiple Parameters

```pseudocode
FUNCTION CalculatePower(
    base AS FLOAT,
    exponent AS INTEGER
) RETURNS FLOAT

    result ← 1

    FOR i ← 1 TO exponent DO
        result ← result * base
    END FOR

    RETURN result

END FUNCTION
```

---

## 26. Default Parameters

```pseudocode
FUNCTION Connect(
    host AS STRING,
    port AS INTEGER = 8080
) RETURNS BOOLEAN
    ...
END FUNCTION
```

Call:

```pseudocode
Connect("localhost")
Connect("localhost", 9000)
```

---

## 27. Optional Parameters

```pseudocode
FUNCTION FindUser(
    id AS INTEGER,
    includeInactive AS BOOLEAN = FALSE
) RETURNS User?
    ...
END FUNCTION
```

`?` indicates the function may return no value.

---

## 28. Pass by Value

```pseudocode
FUNCTION Increment(x AS INTEGER) RETURNS INTEGER
    x ← x + 1
    RETURN x
END FUNCTION
```

---

## 29. Pass by Reference

```pseudocode
PROCEDURE Increment(INOUT x AS INTEGER)
    x ← x + 1
END PROCEDURE
```

---

## 30. Recursive Function

```pseudocode
FUNCTION Factorial(n AS INTEGER) RETURNS INTEGER

    IF n <= 1 THEN
        RETURN 1
    END IF

    RETURN n * Factorial(n - 1)

END FUNCTION
```

---

## 31. Arrays

```pseudocode
numbers ← [10, 20, 30, 40, 50]
```

Access:

```pseudocode
first ← numbers[0]
third ← numbers[2]
```

Modify:

```pseudocode
numbers[1] ← 999
```

Length:

```pseudocode
size ← LENGTH(numbers)
```

---

## 32. Multidimensional Arrays

```pseudocode
matrix ← [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

Access:

```pseudocode
value ← matrix[1][2]
```

---

## 33. Lists

```pseudocode
users ← NEW LIST

users.ADD("Alice")
users.ADD("Bob")
users.ADD("Carol")
```

Remove:

```pseudocode
users.REMOVE("Bob")
```

Check:

```pseudocode
IF users.CONTAINS("Alice") THEN
    PRINT "Found"
END IF
```

---

## 34. Sets

Sets contain unique values:

```pseudocode
tags ← SET("RF", "SDR", "DSP", "RF")
```

Result: `{"RF", "SDR", "DSP"}`

Operations:

```pseudocode
union ← setA UNION setB
intersection ← setA INTERSECT setB
difference ← setA DIFFERENCE setB
```

---

## 35. Dictionary / Map

```pseudocode
user ← {
    "name": "Alice",
    "age": 25,
    "active": TRUE
}
```

Access:

```pseudocode
name ← user["name"]
age ← user["age"]
```

Modify:

```pseudocode
user["age"] ← 26
```

Add:

```pseudocode
user["role"] ← "administrator"
```

Check key:

```pseudocode
IF user.CONTAINS_KEY("role") THEN
    PRINT user["role"]
END IF
```

---

## 36. Dictionary Iteration

```pseudocode
FOR EACH key, value IN user DO
    PRINT key
    PRINT value
END FOR
```

---

## 37. Nested Dictionaries

```pseudocode
system ← {
    "name": "SpectrumMonitor",

    "hardware": {
        "sdr": "HackRF",
        "sampleRate": 20e6
    },

    "software": {
        "language": "C",
        "version": "1.0"
    }
}
```

Access:

```pseudocode
sampleRate ← system["hardware"]["sampleRate"]
```

---

## 38. Structures / Records

```pseudocode
STRUCT Point
    x AS FLOAT
    y AS FLOAT
END STRUCT
```

Create:

```pseudocode
p ← Point(
    x = 10.0,
    y = 20.0
)
```

Access:

```pseudocode
PRINT p.x
PRINT p.y
```

---

## 39. Enumerations

```pseudocode
ENUM Status
    IDLE
    RUNNING
    ERROR
    STOPPED
END ENUM
```

Use:

```pseudocode
status ← Status.RUNNING
```

---

## 40. Classes

```pseudocode
CLASS Person
    name AS STRING
    age AS INTEGER
END CLASS
```

---

## 41. Constructor

```pseudocode
CLASS Person
    name AS STRING
    age AS INTEGER

    CONSTRUCTOR(name, age)
        THIS.name ← name
        THIS.age ← age
    END CONSTRUCTOR

END CLASS
```

---

## 42. Object Creation

```pseudocode
person ← NEW Person("Alice", 25)
```

Access:

```pseudocode
PRINT person.name
PRINT person.age
```

---

## 43. Class Methods

```pseudocode
CLASS Person
    name AS STRING
    age AS INTEGER

    METHOD Introduce()
        PRINT "My name is " + name
        PRINT "I am " + age + " years old"
    END METHOD

END CLASS
```

Call:

```pseudocode
person.Introduce()
```

---

## 44. Instance vs Class/Static Variable

```pseudocode
CLASS Counter
    count AS INTEGER = 0
    STATIC totalCreated AS INTEGER = 0

    CONSTRUCTOR()
        count ← 0
        Counter.totalCreated ← Counter.totalCreated + 1
    END CONSTRUCTOR

END CLASS
```

- `count` — belongs to each object.
- `Counter.totalCreated` — belongs to the class.

---

## 45. Static Method

```pseudocode
CLASS MathUtils

    STATIC METHOD Max(a, b) RETURNS INTEGER
        IF a > b THEN
            RETURN a
        ELSE
            RETURN b
        END IF
    END METHOD

END CLASS
```

Call without creating an object:

```pseudocode
result ← MathUtils.Max(10, 20)
```

---

## 46. Visibility

```pseudocode
CLASS Account
    PUBLIC username AS STRING
    PRIVATE password AS STRING
    PROTECTED balance AS FLOAT
END CLASS
```

| Modifier | Scope |
|----------|-------|
| `PUBLIC` | Accessible everywhere |
| `PRIVATE` | Accessible only inside the class |
| `PROTECTED` | Accessible inside class and subclasses |

---

## 47. Getter / Setter

```pseudocode
CLASS Person
    PRIVATE age AS INTEGER

    METHOD GetAge() RETURNS INTEGER
        RETURN age
    END METHOD

    METHOD SetAge(newAge AS INTEGER)
        IF newAge < 0 THEN
            RAISE InvalidArgumentError("Age cannot be negative")
        END IF
        age ← newAge
    END METHOD

END CLASS
```

---

## 48. Property

```pseudocode
CLASS Person
    PROPERTY age AS INTEGER
        GET
            RETURN _age
        END GET

        SET(value)
            IF value < 0 THEN
                RAISE InvalidArgumentError
            END IF
            _age ← value
        END SET
    END PROPERTY
END CLASS
```

---

## 49. Inheritance

```pseudocode
CLASS Animal
    METHOD Speak()
        PRINT "Some sound"
    END METHOD
END CLASS

CLASS Dog EXTENDS Animal
    METHOD Speak()
        PRINT "Woof"
    END METHOD
END CLASS
```

---

## 50. Polymorphism

```pseudocode
animals ← [
    NEW Dog(),
    NEW Cat(),
    NEW Bird()
]

FOR EACH animal IN animals DO
    animal.Speak()
END FOR
```

The same operation `animal.Speak()` can produce different behavior.

---

## 51. Abstract Class

```pseudocode
ABSTRACT CLASS Shape
    ABSTRACT METHOD Area() RETURNS FLOAT
END CLASS

CLASS Circle EXTENDS Shape
    radius AS FLOAT

    METHOD Area() RETURNS FLOAT
        RETURN PI * radius * radius
    END METHOD
END CLASS
```

---

## 52. Interface

```pseudocode
INTERFACE Serializable
    METHOD Serialize() RETURNS STRING
END INTERFACE
```

Implementation:

```pseudocode
CLASS User IMPLEMENTS Serializable
    METHOD Serialize() RETURNS STRING
        RETURN "{ ... }"
    END METHOD
END CLASS
```

---

## 53. Exception Handling — Basic

```pseudocode
TRY
    result ← Divide(10, 0)
CATCH DivisionByZeroError
    PRINT "Cannot divide by zero"
END TRY
```

---

## 54. Multiple Exceptions

```pseudocode
TRY
    file ← OpenFile("config.json")
    data ← Read(file)
    config ← ParseJSON(data)
CATCH FileNotFoundError
    PRINT "File does not exist"
CATCH ParseError
    PRINT "Invalid JSON"
CATCH Exception
    PRINT "Unexpected error"
END TRY
```

---

## 55. FINALLY

```pseudocode
TRY
    connection ← OpenConnection()
    ExecuteQuery(connection)
CATCH DatabaseError
    PRINT "Database failure"
FINALLY
    CloseConnection(connection)
END TRY
```

`FINALLY` executes regardless of whether an error occurred.

---

## 56. Raise / Throw

```pseudocode
FUNCTION Divide(a, b) RETURNS FLOAT
    IF b = 0 THEN
        RAISE DivisionByZeroError("b cannot be zero")
    END IF
    RETURN a / b
END FUNCTION
```

---

## 57. Custom Exception

```pseudocode
EXCEPTION InvalidConfigurationError
```

Use:

```pseudocode
IF sampleRate <= 0 THEN
    RAISE InvalidConfigurationError(
        "Sample rate must be positive"
    )
END IF
```

---

## 58. Assertions

```pseudocode
ASSERT sampleRate > 0
ASSERT bufferSize > 0
ASSERT user IS NOT NULL
```

Example:

```pseudocode
FUNCTION Process(buffer)
    ASSERT buffer IS NOT NULL
    ASSERT LENGTH(buffer) > 0
    ...
END FUNCTION
```

---

## 59. Null / None

```pseudocode
user ← NULL
```

Checking:

```pseudocode
IF user IS NULL THEN
    PRINT "No user"
END IF
```

Or:

```pseudocode
IF user IS NOT NULL THEN
    PRINT user.name
END IF
```

---

## 60. Optional Result

```pseudocode
FUNCTION FindUser(id) RETURNS OPTIONAL<User>
    ...
END FUNCTION
```

Use:

```pseudocode
user ← FindUser(100)

IF user IS PRESENT THEN
    PRINT user.name
ELSE
    PRINT "User not found"
END IF
```

---

## 61. Error Result (Instead of Exception)

```pseudocode
FUNCTION ReadConfig(path) RETURNS Result
    IF FileDoesNotExist(path) THEN
        RETURN ERROR("File not found")
    END IF

    data ← ReadFile(path)
    RETURN SUCCESS(data)
END FUNCTION
```

Use:

```pseudocode
result ← ReadConfig("config.json")

IF result.IS_ERROR THEN
    PRINT result.error
ELSE
    config ← result.value
END IF
```

---

## 62. Modules

```pseudocode
MODULE DSP
    FUNCTION FFT(signal)
        ...
    END FUNCTION

    FUNCTION PSD(signal)
        ...
    END FUNCTION
END MODULE
```

Use:

```pseudocode
spectrum ← DSP.FFT(signal)
psd ← DSP.PSD(signal)
```

---

## 63. Import

```pseudocode
IMPORT DSP
IMPORT Math
IMPORT FileSystem
```

Or:

```pseudocode
FROM DSP IMPORT FFT
```

---

## 64. Generic Function

```pseudocode
FUNCTION Max<T>(a AS T, b AS T) RETURNS T
    IF a > b THEN
        RETURN a
    ELSE
        RETURN b
    END IF
END FUNCTION
```

Usage:

```pseudocode
Max<INTEGER>(10, 20)
Max<FLOAT>(3.4, 7.2)
```

---

## 65. Generic Class

```pseudocode
CLASS Stack<T>
    items AS LIST<T>

    METHOD Push(value AS T)
        items.ADD(value)
    END METHOD

    METHOD Pop() RETURNS T
        RETURN items.REMOVE_LAST()
    END METHOD
END CLASS
```

---

## 66. Lambda / Anonymous Function

```pseudocode
square ← FUNCTION(x)
    RETURN x * x
END FUNCTION
```

Call:

```pseudocode
result ← square(5)
```

Compact:

```pseudocode
square ← (x) => x * x
```

---

## 67. Map / Filter / Reduce

```pseudocode
numbers ← [1, 2, 3, 4, 5]
```

Map:

```pseudocode
squares ← MAP(numbers, x => x * x)
// Result: [1, 4, 9, 16, 25]
```

Filter:

```pseudocode
even ← FILTER(numbers, x => x MOD 2 = 0)
```

Reduce:

```pseudocode
sum ← REDUCE(numbers, 0, (a, b) => a + b)
```

---

## 68. File Handling — Read

```pseudocode
TRY
    file ← OPEN("data.txt", READ_MODE)
    content ← READ_ALL(file)
    CLOSE(file)
CATCH FileError
    PRINT "Unable to read file"
END TRY
```

---

## 69. File Handling — Write

```pseudocode
file ← OPEN("output.txt", WRITE_MODE)
WRITE(file, "Hello")
WRITE_LINE(file, "World")
CLOSE(file)
```

---

## 70. Resource Management

```pseudocode
USING file ← OPEN("data.txt") DO
    content ← READ_ALL(file)
END USING
```

The resource is automatically closed.

---

## 71. Logging

```pseudocode
LOG.DEBUG("Starting system")
LOG.INFO("Receiver initialized")
LOG.WARNING("Signal weak")
LOG.ERROR("Device unavailable")
```

---

## 72. Configuration

```pseudocode
config ← {
    "centerFrequency": 100.5e6,
    "sampleRate": 2.4e6,
    "gain": 20,
    "fftSize": 4096
}
```

---

## 73. Environment Variables

```pseudocode
path ← ENV["HOME"]
port ← TO_INTEGER(ENV["PORT"])
```

---

## 74. Command-Line Arguments

```pseudocode
FUNCTION Main(args)
    IF LENGTH(args) < 2 THEN
        PRINT "Usage: program <frequency>"
        RETURN 1
    END IF

    frequency ← TO_FLOAT(args[1])
    ...
    RETURN 0
END FUNCTION
```

---

## 75. Return Status

```pseudocode
FUNCTION Initialize() RETURNS INTEGER
    IF HardwareAvailable() = FALSE THEN
        RETURN 1
    END IF
    RETURN 0
END FUNCTION
```

---

## 76. State Machine

```pseudocode
ENUM State
    IDLE
    INITIALIZING
    RUNNING
    ERROR
    STOPPING
END ENUM
```

Algorithm:

```pseudocode
state ← IDLE

WHILE state ≠ STOPPING DO
    SWITCH state

        CASE IDLE:
            IF startRequested THEN
                state ← INITIALIZING
            END IF

        CASE INITIALIZING:
            IF Initialize() = SUCCESS THEN
                state ← RUNNING
            ELSE
                state ← ERROR
            END IF

        CASE RUNNING:
            ProcessData()
            IF failureDetected THEN
                state ← ERROR
            END IF

        CASE ERROR:
            Recover()
            IF recoverySuccessful THEN
                state ← RUNNING
            ELSE
                state ← STOPPING
            END IF

    END SWITCH
END WHILE
```

---

## 77. Events / Callbacks

```pseudocode
FUNCTION OnDataReceived(data)
    Process(data)
END FUNCTION

receiver.ON_DATA ← OnDataReceived
```

Or inline:

```pseudocode
receiver.ON_ERROR ← FUNCTION(error)
    LOG.ERROR(error.message)
END FUNCTION
```

---

## 78. Threads

```pseudocode
THREAD acquisitionThread
    WHILE running DO
        samples ← AcquireSamples()
        buffer.Push(samples)
    END WHILE
END THREAD
```

---

## 79. Synchronization / Mutex

```pseudocode
LOCK mutex
    sharedBuffer.ADD(data)
UNLOCK mutex
```

Equivalent:

```pseudocode
SYNCHRONIZED mutex DO
    sharedBuffer.ADD(data)
END SYNCHRONIZED
```

---

## 80. Semaphore

```pseudocode
WAIT semaphore
    ProcessResource()
SIGNAL semaphore
```

---

## 81. Async / Await

```pseudocode
ASYNC FUNCTION DownloadData(url)
    response ← AWAIT HTTP_GET(url)
    RETURN response
END FUNCTION
```

Call:

```pseudocode
data ← AWAIT DownloadData(url)
```

---

## 82. Parallel Execution

```pseudocode
PARALLEL
    task1 ← START TaskA()
    task2 ← START TaskB()
    task3 ← START TaskC()
END PARALLEL

results ← WAIT_ALL(task1, task2, task3)
```

---

## 83. Timeouts

```pseudocode
result ← WAIT_FOR(
    operation,
    TIMEOUT = 5 seconds
)

IF result = TIMEOUT THEN
    PRINT "Operation timed out"
END IF
```

---

## 84. Retry Logic

```pseudocode
FOR attempt ← 1 TO 3 DO
    TRY
        result ← Connect()
        RETURN result
    CATCH ConnectionError
        WAIT(2 seconds)
    END TRY
END FOR

RAISE ConnectionFailedError
```

---

## 85. Annotations vs Macros

Annotations describe something:

```pseudocode
@static
@deprecated
@override
@private
```

Macros transform or generate code:

```pseudocode
@derive(Serializable)
CLASS User
    ...
END CLASS
```

---

## 86. @static

```pseudocode
CLASS MathUtils
    @static
    FUNCTION Max(a, b)
        IF a > b THEN
            RETURN a
        ELSE
            RETURN b
        END IF
    END FUNCTION
END CLASS
```

Call without instance:

```pseudocode
MathUtils.Max(10, 20)
```

---

## 87. @private

```pseudocode
CLASS User
    @private
    passwordHash AS STRING
END CLASS
```

Restricts external access.

---

## 88. @override

```pseudocode
CLASS Dog EXTENDS Animal
    @override
    METHOD Speak()
        PRINT "Woof"
    END METHOD
END CLASS
```

Communicates intentional replacement of an inherited method.

---

## 89. @abstract

```pseudocode
CLASS Shape
    @abstract
    METHOD Area()
END CLASS
```

---

## 90. @deprecated

```pseudocode
@deprecated("Use NewAPI instead")
FUNCTION OldAPI()
    ...
END FUNCTION
```

---

## 91. @inline

```pseudocode
@inline
FUNCTION Square(x)
    RETURN x * x
END FUNCTION
```

Asks implementation/compiler to inline the call.

---

## 92. @pure

```pseudocode
@pure
FUNCTION Add(a, b)
    RETURN a + b
END FUNCTION
```

Meaning: no side effects; same input → same output.

---

## 93. @threadsafe

```pseudocode
@threadsafe
CLASS RingBuffer
    ...
END CLASS
```

Designed to be safe under concurrent use.

---

## 94. Macro

```pseudocode
MACRO DEBUG_PRINT(value)
    IF DEBUG_MODE THEN
        PRINT("[DEBUG] " + value)
    END IF
END MACRO
```

Usage:

```pseudocode
DEBUG_PRINT("Starting acquisition")
```

---

## 95. Macro Generating Code

```pseudocode
MACRO DEFINE_GETTER(field)
    METHOD Get(field)
        RETURN THIS.field
    END METHOD
END MACRO
```

Then:

```pseudocode
CLASS User
    name AS STRING
    DEFINE_GETTER(name)
END CLASS
```

Expands into:

```pseudocode
METHOD GetName()
    RETURN THIS.name
END METHOD
```

---

## 96. Compile-Time Macro

```pseudocode
@compile_time
MACRO ASSERT_POSITIVE(value)
    IF value <= 0 THEN
        COMPILE_ERROR("Value must be positive")
    END IF
END MACRO
```

---

## 97. Attribute Metadata

Annotations as metadata (not macros):

```pseudocode
@route(
    method = "GET",
    path = "/users"
)
FUNCTION GetUsers()
    ...
END FUNCTION
```

A framework inspects the metadata.

---

## 98. Documentation Annotations

```pseudocode
@doc(
    description = "Calculate signal power",
    units = "dBm"
)
FUNCTION CalculatePower(signal)
    ...
END FUNCTION
```

---

## 99. Realistic Example — Error Handling + Functions + Objects

```pseudocode
CLASS Sensor
    PRIVATE connected AS BOOLEAN

    CONSTRUCTOR()
        connected ← FALSE
    END CONSTRUCTOR

    METHOD Connect() RETURNS BOOLEAN
        TRY
            HardwareConnect()
            connected ← TRUE
            RETURN TRUE
        CATCH HardwareError
            LOG.ERROR("Unable to connect")
            RETURN FALSE
        END TRY
    END METHOD

    METHOD Read() RETURNS Result
        IF connected = FALSE THEN
            RETURN ERROR("Sensor not connected")
        END IF

        TRY
            value ← HardwareRead()
            RETURN SUCCESS(value)
        CATCH HardwareError
            RETURN ERROR("Read failed")
        END TRY
    END METHOD

END CLASS
```
