# BinAnalyze
BinAnalyze is a PyQt5-based application for analyzing binary files using various tools like readelf and hexdump. This application provides a graphical interface to examine the structure and content of binary files, displaying information such as headers, program headers, section headers, symbol tables, and hexdumps.

## Features:
### Upload Functionality:

    Users can upload binary files through a file dialog or by dragging and dropping files onto the application window.

### Analysis Options:

    The application provides several analysis options:
        Header: Displays the header information of the selected binary file.
        Program Headers: Shows the program headers.
        Section Headers: Displays the section headers.
        Symbol Table: Shows the symbol table.
        Hexdump: Provides a hexdump of the binary file.

## Dependencies:
*     PyQt5
*     pyfiglet
*     hexdump (Python package)
*     readelf (Requires installation, typically available in GNU Binutils)
*     

## Installation:
### Clone the repository:
```sh
git clone https://github.com/your_username/BINALYZE.git
```

### Install dependencies:
```sh
sudo apt install binutils
pip install PyQt5 pyfiglet hexdump
```
### Run the application:
```sh
python3 binalyze.py
```

## Screenshots:
[01](/images/01.png)
[02](/images/02.png)
[03](/images/03.png)


## Contributing:
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License:
This project is licensed under the MIT License.
