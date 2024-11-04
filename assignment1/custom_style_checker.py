import ast
import re

class FileAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines_of_code = 0
        self.imports = []
        self.classes = []
        self.functions = []

    def analyze_file_structure(self):
        #read file and count lines
        with open(self.filepath, 'r') as file:
            lines = file.readlines()
            self.lines_of_code = len(lines)

        #parse file
        with open(self.filepath, 'r') as file:
            tree = ast.parse(file.read(), filename=self.filepath)

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node  # Set parent for each child
        
        #walk through each node in the AST to find imports, classes, and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                #handle imports like 'from x import y'
                module = node.module if node.module else ""
                for alias in node.names:
                    self.imports.append(f"{module}.{alias.name}")
            elif isinstance(node, ast.ClassDef):
                 # Add each class with name and docstring to the classes list
                class_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node),  # Extracts the class's docstring if it exists
                    'methods': []
                }
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef):
                        method_info = {
                            'name': class_node.name,
                            'docstring': ast.get_docstring(class_node),
                            'args': [{'name': arg.arg, 'annotation': self._annotation_to_string(arg.annotation)} for arg in class_node.args.args],
                            'returns': self._annotation_to_string(class_node.returns)
                        }
                        class_info['methods'].append(method_info)
                self.classes.append(class_info)
            elif isinstance(node, ast.FunctionDef):
                # Check if the function is a standalone function (not inside a class)
                if not isinstance(getattr(node, 'parent', None), ast.ClassDef):
                    function_info = {
                        'name': node.name,
                        'docstring': ast.get_docstring(node),  # Extracts the function's docstring if it exists
                        'args': [{'name': arg.arg, 'annotation': self._annotation_to_string(arg.annotation)} for arg in node.args.args],
                        'returns': self._annotation_to_string(node.returns)
                    }
                    self.functions.append(function_info)
    def _annotation_to_string(self, annotation):
        """Convert annotation AST node to a string or return None if not annotated."""
        if annotation is None:
            return None
        elif isinstance(annotation, ast.Name):
            return annotation.id  # Simple types like 'int' or 'float'
        elif isinstance(annotation, ast.Attribute):
            return f"{annotation.value.id}.{annotation.attr}"  # Handle qualified types
        elif isinstance(annotation, ast.Subscript):
            # Handle subscripted types (like 'List[int]')
            return f"{annotation.value.id}[{annotation.slice.value.id}]"
        return None  # For unsupported or complex cases, return None as unannotated
    def get_file_structure_report(self):
        # Returns a formatted string report of the file structure analysis
        report = f"Total lines of code: {self.lines_of_code}\n"
        report += "Imports:\n" + "\n".join(f"- {imp}" for imp in self.imports) + "\n"
        
        # Format classes and their methods
        report += "Classes:\n"
        for cls in self.classes:
            report += f"- {cls['name']}: {cls['docstring'] or 'DocString not found'}\n"  # Display class name and docstring
            for method in cls['methods']:
                report += f"  - Method '{method['name']}': {method['docstring'] or 'DocString not found'}\n"  # Display each method's name and docstring
        
        # Format standalone functions
        report += "Functions:\n"
        report += "\n".join(f"- {func['name']}: {func['docstring'] or 'DocString not found'}" for func in self.functions) + "\n"  # Display each function's name and docstring
        
        return report


class DocStringChecker:
    def __init__(self, classes, functions):
        self.classes = classes
        self.functions = functions
        self.docstring_results = []

    def check_docstrings(self):
        # analyze each class for docstring
        for cls in self.classes:
            if cls['docstring']:
                self.docstring_results.append(f"Class '{cls['name']}': {cls['docstring']}")
            else:
                self.docstring_results.append(f"Class '{cls['name']}': DocString not found")
        
        # analyze each function for docstring
        for func in self.functions:
            if func['docstring']:
                self.docstring_results.append(f"Function '{func['name']}': {func['docstring']}")
            else:
                self.docstring_results.append(f"Function '{func['name']}': DocString not found")
    
    def get_docstring_report(self):
        return "\n".join(self.docstring_results)



class TypeAnnotationChecker:
    def __init__(self, functions, classes):
        self.functions = functions  # List of standalone functions
        self.classes = classes      # List of classes with methods
        self.missing_annotations = []  # List to store functions and methods without type annotations

    def check_type_annotations(self):
        # Check standalone functions
        for func in self.functions:
            if not self._has_type_annotations(func):
                self.missing_annotations.append(f"Function '{func['name']}'")

        # Check methods in each class
        for cls in self.classes:
            for method in cls['methods']:
                if not self._has_type_annotations(method):
                    self.missing_annotations.append(f"Method '{method['name']}' in class '{cls['name']}'")

    def _has_type_annotations(self, func):
        # Returns True if the function has type annotations for all args and return type
        args_annotated = all(arg['annotation'] is not None for arg in func['args'])
        return_annotation = func['returns'] is not None

        return args_annotated and return_annotation

    def get_annotation_report(self):
        if not self.missing_annotations:
            return "All functions and methods have type annotations.\n"
        else:
            report = "Missing Type Annotations:\n"
            report += "\n".join(f"- {item}" for item in self.missing_annotations)
            return report + "\n"


class NamingConventionChecker:
    def __init__(self, classes, functions):
        self.classes = classes
        self.functions = functions
        self.naming_issues = {
            'classes': [],
            'functions': []
        }

    def check_naming_conventions(self):
        # Check class names for CamelCase
        for cls in self.classes:
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', cls['name']):  # Class should match CamelCase
                self.naming_issues['classes'].append(f"Class '{cls['name']}' does not follow CamelCase")

        # Check function and method names for snake_case
        for func in self.functions:
            if not re.match(r'^[a-z_][a-z0-9_]*$', func['name']):  # Function should match snake_case
                self.naming_issues['functions'].append(f"Function '{func['name']}' does not follow snake_case")
        
        # Check methods within each class
        for cls in self.classes:
            for method in cls['methods']:
                if not re.match(r'^[a-z_][a-z0-9_]*$', method['name']):  # Method should match snake_case
                    self.naming_issues['functions'].append(f"Method '{method['name']}' in class '{cls['name']}' does not follow snake_case")

    def get_naming_report(self):
        # Return the formatted report of naming convention issues
        if not self.naming_issues['classes'] and not self.naming_issues['functions']:
            return "All names adhere to the specified naming convention.\n"
        
        report = "Naming Convention Issues:\n"
        if self.naming_issues['classes']:
            report += "Classes:\n" + "\n".join(f"- {issue}" for issue in self.naming_issues['classes']) + "\n"
        if self.naming_issues['functions']:
            report += "Functions and Methods:\n" + "\n".join(f"- {issue}" for issue in self.naming_issues['functions']) + "\n"
        
        return report


class StyleReport:
    def __init__(self, file_analyzer, docstring_checker, type_checker, naming_checker):
        self.file_analyzer = file_analyzer
        self.docstring_checker = docstring_checker
        self.type_checker = type_checker
        self.naming_checker = naming_checker

    def generate_report(self):
        # Placeholder: Logic to compile results and write report
        pass

def main(filepath):
     # Step 1: Initialize FileAnalyzer and analyze file structure
    file_analyzer = FileAnalyzer(filepath)
    file_analyzer.analyze_file_structure()

    # Display the file structure for testing purposes
    print("File Structure Analysis:")
    print(file_analyzer.get_file_structure_report())
    print("\n" + "="*40 + "\n")

    # Step 2: Initialize DocStringChecker with identified classes and functions
    # We will pass file_analyzer's classes and functions to the DocStringChecker
    docstring_checker = DocStringChecker(file_analyzer.classes, file_analyzer.functions)
    docstring_checker.check_docstrings()

    # Display docstring analysis for testing purposes
    print("Docstring Analysis:")
    print(docstring_checker.get_docstring_report())
    print("\n" + "="*40 + "\n")

    # Step 3: Initialize TypeAnnotationChecker with functions
    # We will use the functions identified in file_analyzer to check for type annotations
    type_checker = TypeAnnotationChecker(file_analyzer.functions, file_analyzer.classes)
    type_checker.check_type_annotations()

    # Display type annotation analysis for testing purposes
    print("Type Annotation Analysis:")
    print(type_checker.get_annotation_report())
    print("\n" + "="*40 + "\n")

    # Step 4: Initialize NamingConventionChecker with classes and functions
    # This checker will verify that class and function names follow the specified conventions
    naming_checker = NamingConventionChecker(file_analyzer.classes, file_analyzer.functions)
    naming_checker.check_naming_conventions()

    # Display naming convention analysis for testing purposes
    print("Naming Convention Analysis:")
    print(naming_checker.get_naming_report())
    print("\n" + "="*40 + "\n")

    # Step 5: Generate the report
    # Once all checks are completed, we use StyleReport to create a consolidated report
    report = StyleReport(file_analyzer, docstring_checker, type_checker, naming_checker)
    report.generate_report()

    # Inform the user that the report has been created
    print(f"Style report generated: style_report_{filepath}.txt")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python style_checker.py <path_to_python_file>")
    else:
        main(sys.argv[1])