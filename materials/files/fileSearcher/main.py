from pathlib import Path
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text

# Create a global console object for colorized output
console = Console()



def is_hidden(path):
    """Check if any part of the path is hidden (starts with .)
    
    Args:
        path: A Path object representing a file or directory
        
    Returns:
        bool: True if any part of the path starts with a dot
    """
    return any(part.startswith('.') and part not in ['.', '..'] 
               for part in path.parts)
# End of is_hidden()




def getPath(myFileType="*", full_search=False):
    """Get all files in the current directory and subdirectories.
    
    Args:
        myFileType: File pattern to match (default: all files)
        full_search: If True, include hidden files/directories
        
    Returns:
        list: List of Path objects for matching files
    """
    # Create a Path object for the directory
    base_path = Path('./')
    
    if full_search:
        myFiles = [p for p in base_path.rglob(myFileType) 
                   if p.is_file()]
    else:
        myFiles = [p for p in base_path.rglob(myFileType) 
                   if p.is_file() and not is_hidden(p)]
    
    return myFiles
# End of getPath()



def searchFilenames(myPath, searchTerm, full_search=False):
    """Search for files with searchTerm in their filename.
    
    Args:
        myPath: Directory path to search in
        searchTerm: String to search for in filenames
        full_search: If True, include hidden files/directories
        
    Returns:
        list: List of Path objects for matching files
    """
    # Create a Path object for the directory
    base_path = Path(myPath)
    
    if full_search:
        myFiles = [p for p in base_path.rglob("*") 
                   if p.is_file() and searchTerm in p.name]
    else:
        myFiles = [p for p in base_path.rglob("*") 
                   if p.is_file() 
                   and searchTerm in p.name 
                   and not is_hidden(p)]
    
    return myFiles
# End of searchFilenames()




def searchFileContents(myPath, searchTerm, myFileType="*", 
                      full_search=False):
    """Search for files containing searchTerm in their contents.
    
    Args:
        myPath: Directory path to search in
        searchTerm: String to search for in file contents
        myFileType: File pattern to match (default: all files)
        full_search: If True, include hidden files/directories
        
    Returns:
        list: List of Path objects for matching files
    """
    # Create a Path object for the directory
    base_path = Path(myPath)
    
    myFiles = []
    for p in base_path.rglob(myFileType):
        if p.is_file():
            # Skip hidden files/directories unless full_search is enabled
            if not full_search and is_hidden(p):
                continue
            try:
                with p.open() as f:
                    if searchTerm in f.read():
                        myFiles.append(p)
            except Exception as e:
                console.print(f"[yellow]Warning: Error reading file {p}: {e}[/yellow]")
    
    return myFiles
# End of searchFileContents()






def printFileContents(filePath):
    """Display file contents with syntax highlighting.
    
    Args:
        filePath: Path object or string path to the file
    """
    try:
        with open(filePath) as f:
            content = f.read()
            # Try to detect file type for syntax highlighting
            suffix = filePath.suffix.lstrip('.')
            
            # List of supported languages for syntax highlighting
            if suffix in ['py', 'js', 'java', 'cpp', 'c', 'rs', 'go', 
                         'rb', 'php', 'html', 'css', 'json', 'xml', 
                         'yaml', 'yml', 'toml', 'md', 'sh', 'bash']:
                syntax = Syntax(content, suffix, theme="monokai", 
                              line_numbers=True)
                console.print(Panel(syntax, title=f"[cyan]{filePath}[/cyan]", 
                                  border_style="blue"))
            else:
                console.print(Panel(content, title=f"[cyan]{filePath}[/cyan]", 
                                  border_style="blue"))
    except Exception as e:
        console.print(f"[red]Error reading file {filePath}: {e}[/red]")
# End of printFileContents()





def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description='Search for files by filename or file contents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py --filename test
  python main.py --filecontents "import sys"
  python main.py --filename test --filecontents python
        '''
    )
    
    parser.add_argument(
        '--filename',
        type=str,
        help='Search term to find in filenames'
    )
    
    parser.add_argument(
        '--filecontents',
        type=str,
        help='Search term to find in file contents'
    )

    parser.add_argument(
        '--path',
        type=str,
        default='./',
        help='Base path to search (default: current directory)'
    )
    
    parser.add_argument(
        '--full-search',
        action='store_true',
        help='Include hidden files and directories (those starting with .)'
    )
    
    args = parser.parse_args()
    
    # Display search mode
    if args.full_search:
        console.print("[bold yellow]Search mode: FULL (including hidden files/directories)[/bold yellow]\n")
    else:
        console.print("[bold green]Search mode: NORMAL (excluding hidden files/directories)[/bold green]")
        console.print("[dim]Tip: Use --full-search to include hidden files and directories[/dim]\n")


    # If no arguments provided, show all files
    if not args.filename and not args.filecontents:
        myFiles = getPath(full_search=args.full_search)
        console.print(Panel("[bold cyan]All files in the current directory and subdirectories[/bold cyan]", 
                          border_style="cyan"))
        
        if myFiles:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=6)
            table.add_column("File Path", style="cyan")
            
            for idx, file_path in enumerate(myFiles, 1):
                table.add_row(str(idx), str(file_path))
            
            console.print(table)
            console.print(f"\n[bold green]Total: {len(myFiles)} files found[/bold green]")
        else:
            console.print("[yellow]No files found.[/yellow]")
        
        console.print("\n[dim]Tip: Use --filename or --filecontents to search for specific files[/dim]")
        console.print("[dim]Run with --help for more information[/dim]")

    # Search by filename if provided
    if args.filename:
        myFiles = searchFilenames(args.path, args.filename, 
                                 full_search=args.full_search)
        console.print(Panel(f"[bold cyan]Files containing '{args.filename}' in their name[/bold cyan]", 
                          border_style="cyan"))
        
        if myFiles:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=6)
            table.add_column("File Path", style="green")
            
            for idx, file_path in enumerate(myFiles, 1):
                table.add_row(str(idx), str(file_path))
            
            console.print(table)
            console.print(f"\n[bold green]Total: {len(myFiles)} files found[/bold green]")
        else:
            console.print("[yellow]No files found.[/yellow]")

    # Search by file contents if provided
    if args.filecontents:
        myFiles = searchFileContents(args.path, args.filecontents, 
                                    full_search=args.full_search)
        console.print(Panel(f"[bold cyan]Files containing '{args.filecontents}' in their contents[/bold cyan]", 
                          border_style="cyan"))
        
        if myFiles:
            console.print(f"[bold green]Found {len(myFiles)} file(s)[/bold green]\n")
            for idx, file_path in enumerate(myFiles, 1):
                console.print(f"[bold yellow]{idx}. {file_path}[/bold yellow]")
                printFileContents(file_path)
                console.print()  # Add spacing between files
        else:
            console.print("[yellow]No files found.[/yellow]")
    
    console.print("[bold green]✓ Done.[/bold green]")

# End of main()





if __name__ == "__main__":
    main()
