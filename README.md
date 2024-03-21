# 1. Introduction
This interpreter serves as a bridge between rule declarations written in YAML format and executable Python code within OpExpert. It supports six fundamental operations crucial for setting rules within the OpExpert environment: Conditions, Executions, Functions, Imports, Integrations, and Modules. Each operation corresponds to a specific aspect of rule definition and execution.

- Conditions: Specifies the conditions under which a rule should be triggered or applied.
- Executions: Executes a function.
- Functions: Imports a code snippet from the OpExpert environment and stores it as a function that can be executed later.
- Imports: Imports packages within the Python environment.
- Integrations: A list or records where each record is a dictionary.
- Modules: A dictionary that may hold required information.

<br>

***
*[Section 3.1](#31-formatting-your-yaml-script) of this documentation provides detailed instructions on how to format the YAML file correctly to define rules using these supported operations. By adhering to the specified format, users can seamlessly translate their rule definitions from YAML into Python code, ensuring compatibility and effectiveness within the OpExpert environment.*

<br>
<br>
<br>

# 2. Installation and Setup
The installation and setup process for this interpreter are straightforward. Follow the steps below to ensure a proper setup:

<br>

- Step 1: Fork this repository and store it in a local environment.
    
    - Start by navigating to the repository on GitHub.

    - Click on the "Fork" button in the upper-right corner to create a copy of the repository under your GitHub account.
    
    - Clone the forked repository to your local environment using Git or download it as a ZIP file and extract it.

<br>

- Step 2: Install required modules.

    - Before proceeding, ensure you have Python installed on your system.
    - Navigate to the root directory of the cloned or extracted repository in your terminal or command prompt.
    - Run the following command in your terminal to install the required modules:
    
        > pip install -r requirements.txt

<br>
<br>
<br>

# 3. Getting started

This section serves as a comprehensive guide to understanding the formatting structure of YAML scripts and how to interpret them using the provided code to create an executable Python script.

<br>

## 3.1. Formatting your YAML script

This section begins by discussing the essential task of specifying the type of operation within your YAML script. As outlined in [Section 1](#1-introduction), there are six possible operations, each identified by the key type within your YAML script.

We'll now outline the format for each type of operation and provide clear instructions on how to properly structure them.

<br>

### 3.1.1. Types of Operations: Imports

`import` operations can be placed anywhere within the rule script. However, it's recommended to include them at the beginning of the script to ensure their scope availability throughout the code. This operation exclusively supports **Python packages.**

```yaml
- type:                         import                      [required]
  importName:                   <String>                    [required]
  packageName:                  <String>                    [optional]
  alias:                        <String>                    [optional]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `importName` is a **required** parameter that defines the name of the package that requires importing.

- `packageName` is an optional parameter that specifies the name of the package during installation. Certain packages may have different import names compared to their installation names. If the names match, this parameter can be omitted.

- `alias` is an optional parameter used to specify the name under which you'd like to import the package. If not specified, the package's name can be used for reference.

<br>

### 3.1.2. Types of Operations: Integrations

```yaml
- type:                         integration                 [required]
  alias:                        <String>                    [required]
  recordID:                     <String>                    [required]
  params:                                                   [optional]
    - from:                     <String>                    [optional]
    - till:                     <String>                    [optional]
    - maxRecords:               <String>                    [optional]
    - includeDeleted:           <String>                    [optional]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `alias` is a **required** parameter serving as the variable name storing the returned integration.

- `recordID` is a **required** parameter used to pass the record ID of the integration module to retrieve.

- `params` is an **optional** parameter allowing specification of filters to apply on the fetched integration. Multiple filters may be specified as shown above.

<br>

### 3.1.3. Types of Operations: Modules

```yaml
- type:                         module                      [required]
  alias:                        <String>                    [required]
  recordID:                     <String>                    [required]
  moduleName:                   <String>                    [required]
  fields:                                                   [required]
    - field                     <String>                    [required]
    - field                     <String>                    [required]
    - field                     <String>                    [required]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `alias` is a **required** parameter serving as the variable name storing the returned integration.

- `recordID` is a **required** parameter used to pass the record ID of the module to retrieve.

- `moduleName` is a **required** parameter used to pass the name of the module to retrieve from.

- `fieldName` is a **required** parameter used to pass the name of the field to retrieve teh data from.

- `params` is an **optional** parameter allowing specification of filters to apply on the fetched module. Multiple filters may be specified as shown above.

When a *module* action is invoked, it can return two different types of values depending on the case.

- When **no field has been specified or multiple fields have been requested,** a dictionary containing the key-value pairs of all the fields, or the specified fields respectively, will be returned. 
These values can be referred to just like a normal dictionary in Python, using the syntax `alias['key']`.

- When **only a single field has been requested,** only the value of that specific field is returned and stored as a string. This can simply be referred to using the syntax `alias`.

<br>

### 3.1.4. Types of Operations: Functions

```yaml
- type:                         function                    [required]
  fName:                        <String>                    [required]
  recordID:                     <String>                    [required]
  args:                                                     [optional]
    - argument                  <String>                    [optional]
    - argument                  <String>                    [optional]
    - argument                  <String>                    [optional]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `fName` is a **required** parameter specifying the name of the function for later reference.

- `recordID` is a **required** parameter used to pass the record ID of the function module to retrieve.

- `args` is an **optional** parameter used to specify the variable name for the arguments of the function being created, if applicable. If the function does not require any arguments, this parameter can be omitted. Type conversions for these arguments must be managed within the code snippet being fetched.

<br>

### 3.1.5. Types of Operations: Executions

Ideally, we have two distinct methods of passing a parameter to a function. We can either utilize a variable that stores the parameter or directly pass in the parameter as a value.

<br>

#### A. Passing a variable

```yaml
- type:                         execute                     [required]
  alias:                        <String>                    [optional]
  fName:                        <String>                    [required]
  params:                                                   [optional]
    - pType:                    reference                   [required]
      pValue:                   <String>                    [required]
    - pType:                    reference                   [required]
      pValue:                   <String>                    [required]
    - pType:                    reference                   [required]
      pValue:                   <String>                    [required]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `alias` is an **optional** parameter that stores the return value of the function, if applicable.

- `fName` is a **required** parameter specifying the name of the function to call.

- `params` is an **optional** parameter used to specify the parameters if the function requires any.
  - `pType` is a **required** parameter used to specify the type of value being passed, indicating whether it is a reference to another variable or an actual value. You mention `reference` to indicate that you're passing a variable and not a direct value.
  - `pValue` is a **required** parameter used to specify the value. If referring to a variable, provide the variable name. If it's a direct value, simply provide the value.

<br>

#### B. Passing a direct value

```yaml
- type:                         execute                     [required]
  alias:                        <String>                    [optional]
  fName:                        <String>                    [required]
  params:                                                   [optional]
    - pType:                    value                       [required]
      pValue:                   <String>                    [required]
    - pType:                    value                       [required]
      pValue:                   <String>                    [required]
    - pType:                    value                       [required]
      pValue:                   <String>                    [required]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `alias` is an **optional** parameter that stores the return value of the function, if applicable.

- `fName` is a **required** parameter specifying the name of the function to call.

- `params` is an **optional** parameter used to specify the parameters if the function requires any.
  - `pType` is a **required** parameter used to specify the type of value being passed, indicating whether it is a reference to another variable or an actual value. You mention `value` to indicate that you're passing a direct value and not a variable.
  - `pValue` is a **required** parameter used to specify the value. If referring to a variable, provide the variable name. If it's a direct value, simply provide the value.

<br>

### 3.1.6. Types of Operations: Conditions

```yaml
- type:                         condition                   [required]
  condition:                    <String>                    [required]
  action:                                                   [required]
    - type:                     <Type>                      [required]
    - type:                     <Type>                      [optional]
    - type:                     <Type>                      [optional]
```

- `type` is a **required** parameter that defines the type of operation being performed.

- `condition` is a **required** parameter that specifies the condition that must be satisfied.

- `action` is a **required** parameter that specifies the action to be executed upon satisfying a condition.
  - Within the `action` keyword, the `type` parameter can be any of the previously mentioned types, provided they adhere to their respective syntax as outlined.
  - At least one type of action must be provided. However, subsequent actions for satisfying the condition are optional.
  - Two actions of type `condition` must not exist within the same hierarchy if there is a reference to the same integration in either condition.

Different variables are referenced in various ways. Here's how you can refer to each of them:

- **Integrations**
  <br>
  When a variable or alias contains an Integration returned by the script, it's stored in the form of a list. Each record within this list is represented as a dictionary. To simplify conditional operations on these records, the structure has been designed to facilitate ease of use. When used in the statement under the *condition* keyword, you can refer to the key of the record simply as `integration['key']`, in which case the statement would look like `IF integration['key'] = value`.
  <br>
  When you need to use the value that has satisfied a condition in a subsequent action, you can simply refer to it in a similar manner by using `integration['key']`.

- **Modules**
  <br>
  As of now, Modules cannot be used in conditional statements, as it may conflict with the use of Integrations.

<br>


Conditions can be categorized into three types, each serving a specific use case:

- IF: This condition is used to specify a block of code to be executed if the given condition is true. It's the initial check in a series of conditions.

- ELIF: Short for "else if", this condition is used to specify a new condition to test if the previous conditions were not true. It's used when there are multiple conditions to be checked in a sequence after the initial IF condition. It is necessary that the `ELIF` statement is used in the same hierarchy as a previous `IF` statement. It cannot be used independently; it must follow an `IF` statement that has been previously mentioned under the same hierarchy.

- ELSE: This condition is used to specify a block of code to be executed if none of the preceding conditions are true. It's the final fallback option in a series of conditions. It is necessary that the `ELSE` statement is used in the same hierarchy as a previous `IF` statement. It cannot be used independently; it must follow an `IF` statement that has been previously mentioned under the same hierarchy.

<br>

The condition keyword will contain the statement that needs to be satisfied. Here are the conditional operators that can be used and their meanings:

- `AND` is used as a Logical AND operator, requires both conditions to be true.

- `OR` is used as a Logical OR operator, requires at least one condition to be true.

- `NOT` is used as a Logical NOT operator, negates the condition.

- `=` is used as a Equality operator, checks if two values are equal.

- `>` is used as a Greater than operator, checks if one value is greater than another.

- `<` is used as a Less than operator, checks if one value is less than another.

- `>=` is used as a Greater than or equal to operator, checks if one value is greater than or equal to another.

- `<=` is used as a Less than or equal to operator, checks if one value is less than or equal to another.

<br>

With this knowledge, the statement can be structured similarly to how Python 'IF' statements are organized. The structured statement can then be provided under the `conditon` key in the YAML script.

<br>

## 3.2. Interpreting your YAML script

Interpreting your YAML script involves parsing the YAML data and converting it into executable Python code. This process is facilitated by the provided code in the repository, specifically the `LanguageInterpreter` class. To interpret the YAML script:

<br>

- Step 1: Import the `LanguageInterpreter.py` module into your Python environment.

- Step 2: Create an object of the `LanguageInterpreter` class, passing username, password, and the path to your YAML script or the record ID of a function stored within the OpExpert environment as an argument.

- Step 3: The interpreter will parse the YAML data and generate corresponding Python code, based on the defined operations and conditions. While the process isn't automatic, it's necessary to call the `processPayload()` method of the object.

- Step 4: You can either print the generated Python code or execute it using the methods `printInterpretedText()` or `executeInterpretedText()` respectively.