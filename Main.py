import json
import csv
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
import unicodedata
import re

# from enum import Enum

# class SupportedFormats(Enum):
#     CSV = ".csv"
#     JSON = ".json"


# ========================================
#    CLASE ABSTRACTA PRINCIPAL            #
# ========================================
class DataConverter(ABC):
    def __init__(self, filePath: str):
        self.filePath = filePath
        self.data = []
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"Archivo no encontrado: {filePath}")
    
    @abstractmethod
    def readData(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def writeData(self, outputPath: str) -> bool:
        pass
    
    @abstractmethod
    def validateFormat(self) -> bool:
        pass

# ========================================
#    IMPLEMENTACIÓN PARA CSV              #
# ========================================
class CSVConverter(DataConverter):
    def __init__(self, filePath: str, delimiter: str = ','):
        super().__init__(filePath)
        self.delimiter = delimiter
    
    def readData(self) -> List[Dict[str, Any]]:
        with open(self.filePath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)
            self.data = [row for row in reader]
        return self.data
    
    def writeData(self, outputPath: str) -> bool:
        if not self.data:
            return False
        
        # Crear directorios si no existen
        directory = os.path.dirname(outputPath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        with open(outputPath, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys(), delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(self.data)
        return True
    
    def validateFormat(self) -> bool:
        try:
            with open(self.filePath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=self.delimiter)
                return next(reader, None) is not None
        except:
            return False

# ========================================
#    IMPLEMENTACIÓN PARA JSON             #
# ========================================
class JSONConverter(DataConverter):
    def readData(self) -> List[Dict[str, Any]]:
        with open(self.filePath, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        return self.data
    
    def writeData(self, outputPath: str) -> bool:
        # Crear directorios si no existen
        directory = os.path.dirname(outputPath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        with open(outputPath, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
        return True
    
    def validateFormat(self) -> bool:
        try:
            with open(self.filePath, 'r', encoding='utf-8') as file:
                json.load(file)
                return True
        except:
            return False

# ========================================
#    NORMALIZACIÓN DE TEXTO Y DATOS       #
# ========================================
class TextNormalizer:
    @staticmethod
    def removeAccents(text: str) -> str:
        if not isinstance(text, str):
            return text
            
        normalized = unicodedata.normalize('NFD', text)
        return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    
    @staticmethod
    def normalizeText(text: str) -> str:
        if not isinstance(text, str):
            return text
            
        text = TextNormalizer.removeAccents(text)
        return text.lower().strip()
    
    @staticmethod
    def normalizeKey(key: str) -> str:
        if not isinstance(key, str):
            return key
            
        key = TextNormalizer.removeAccents(key)
        key = re.sub(r'[^a-zA-Z0-9_]', '_', key)  
        return key.lower()
    
    @staticmethod
    def cleanData(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleanedData = []
        
        for item in data:
            cleanedItem = {}
            for key, value in item.items():
                normalizedKey = TextNormalizer.normalizeKey(key)
                
                if isinstance(value, str):
                    cleanedValue = TextNormalizer.normalizeText(value)
                else:
                    cleanedValue = value
                
                if cleanedValue is None or cleanedValue == "":
                    cleanedValue = "n/a"
                
                cleanedItem[normalizedKey] = cleanedValue
            
            cleanedData.append(cleanedItem)
        
        return cleanedData

# ========================================
#    CONVERSOR PRINCIPAL                  #
# ========================================
class FileConverter:
    @staticmethod
    def getConverter(filePath: str):
        ext = os.path.splitext(filePath)[1].lower()
        if ext == '.csv':
            return CSVConverter(filePath)
        elif ext == '.json':
            return JSONConverter(filePath)
        else:
            raise ValueError(f"Formato no compatible: {ext}")
    
    @staticmethod
    def convert(inputPath: str, outputPath: str) -> bool:
        if not os.path.exists(inputPath):
            raise FileNotFoundError(f"Archivo de entrada no existe: {inputPath}")
        
        inputConverter = FileConverter.getConverter(inputPath)
        if not inputConverter.validateFormat():
            raise ValueError("Formato de entrada inválido")
        
        data = inputConverter.readData()
        cleanedData = TextNormalizer.cleanData(data)
        
        outputConverter = FileConverter.getConverter(outputPath)
        outputConverter.data = cleanedData
        return outputConverter.writeData(outputPath)

# ========================================
#    EJEMPLO DE USO                       #
# ========================================
class ExampleUsage:
    @staticmethod
    def run():
        try:
            success = FileConverter.convert("output.json","Notion.csv")
            if success:
                print("✓ Conversion successful! File saved as output.json")
            else:
                print("✗ Conversion failed. Please check the input file format.")
        except Exception as e:
            print(f"Error: {e}")
            
if __name__ == "__main__":
    ExampleUsage.run()
        
# ╔══════════════════════════════════════════════════════════════════╗
# ║       REFERENCIA PRINCIPAL  - FromCSVtoJSON\test.csv             ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║ - La línea 1 asocia campos con títulos y será la base para este  ║
# ║  script.                                                         ║
# ║   - modificalo según tus necesidades.                            ║
# ║ - Las líneas siguientes son datos de ejemplo.                    ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝