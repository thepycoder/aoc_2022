use std::{fs::File, io::{BufReader, BufRead}};
use itertools::Itertools;


pub fn day4_1(filepath: &str) -> Result<u32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let mut total = 0;
    
    for line in reader.lines() {
        let sections = line.unwrap();
        let elf_pairs: Vec<&str> = sections.split(',').collect();
        for (elf_1, elf_2) in elf_pairs.into_iter().tuples() {
            let elf_1_parsed: Vec<u32> = elf_1.split("-").map(|nr| nr.parse::<u32>().unwrap()).collect();
            let elf_2_parsed: Vec<u32> = elf_2.split("-").map(|nr| nr.parse::<u32>().unwrap()).collect();

            // dbg!(&elf_1_parsed);
            // dbg!(&elf_2_parsed);
            
            if elf_1_parsed[0] <= elf_2_parsed[0] && elf_1_parsed[1] >= elf_2_parsed[1] {
                total += 1;
                // dbg!("Added");
            } else if elf_1_parsed[0] >= elf_2_parsed[0] && elf_1_parsed[1] <= elf_2_parsed[1] {
                total += 1;
                // dbg!("Added");
            }
        }
    }
    Ok(total)
}

pub fn day4_2(filepath: &str) -> Result<u32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let mut total = 0;
    
    for line in reader.lines() {
        let sections = line.unwrap();
        let elf_pairs: Vec<&str> = sections.split(',').collect();
        for (elf_1, elf_2) in elf_pairs.into_iter().tuples() {
            let elf_1_parsed: Vec<u32> = elf_1.split("-").map(|nr| nr.parse::<u32>().unwrap()).collect();
            let elf_2_parsed: Vec<u32> = elf_2.split("-").map(|nr| nr.parse::<u32>().unwrap()).collect();

            // dbg!(&elf_1_parsed);
            // dbg!(&elf_2_parsed);
            
            if elf_1_parsed[0] <= elf_2_parsed[0] && elf_1_parsed[1] >= elf_2_parsed[1] {
                total += 1;
                // dbg!("Added");
            } else if elf_1_parsed[0] >= elf_2_parsed[0] && elf_1_parsed[1] <= elf_2_parsed[1] {
                total += 1;
                // dbg!("Added");
            } else if elf_1_parsed[0] <= elf_2_parsed[0] && elf_2_parsed[0] <= elf_1_parsed[1] && elf_1_parsed[1] <= elf_2_parsed[1] {
                total += 1;
            } else if elf_1_parsed[0] >= elf_2_parsed[0] && elf_1_parsed[0] <= elf_2_parsed[1] && elf_1_parsed[1] >= elf_2_parsed[1] {
                total += 1;
            }
        }
    }
    Ok(total)
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day4_1() {
        assert_eq!(day4_1("data/test4_1.txt").unwrap(), 2);
    }

    #[test]
    fn test_day4_2() {
        assert_eq!(day4_2("data/test4_1.txt").unwrap(), 4);
    }
}