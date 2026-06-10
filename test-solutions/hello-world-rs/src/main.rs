use std::fs;
use std::io;

fn main() -> io::Result<()> {
    let name = fs::read_to_string("name.txt")?;
    let name = name.trim_end_matches(['\r', '\n']);
    fs::write("hello.txt", format!("hello {name}\n"))
}
