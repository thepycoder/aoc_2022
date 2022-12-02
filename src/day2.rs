use std::fs::File;
use std::io::{BufReader, BufRead};


pub fn day2_1(filepath: &str) -> Result<i32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let lines: Vec<String> = reader.lines().map(|s| s.expect("Could not read line!")).collect();
    // println!("{:?}", lines);
    let array: Vec<Vec<i32>> = lines.iter().map(|line| line.replace(" ", "").chars().map(
        |x| match x { 
            'A' | 'X' => 1, 
            'B' | 'Y' => 2, 
            'C' | 'Z' => 3,
            _ => -1
        }).collect()).collect();
    // println!("{:?}", array);

    let scores: Vec<i32> = array.iter().map(
        // The score of the game is the value of whatever you played
        |single_game| single_game[1] 
        // + 6 if you won, 0 if you didn't
        + 6 * (single_game[1] - 1 == (single_game[0] % 3)) as i32
        // + 3 if it was a tie. This line and previous line will never fire at the same time
        + 3 * (single_game[0] == single_game[1]) as i32
    ).collect();

    // println!("{:?}", scores);

    Ok(scores.iter().sum())
}



pub fn day2_2(filepath: &str) -> Result<i32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let lines: Vec<String> = reader.lines().map(|s| s.expect("Could not read line!")).collect();
    // println!("{:?}", lines);
    let array: Vec<Vec<i32>> = lines.iter().map(|line| line.replace(" ", "").chars().map(
        |x| match x { 
            'A' | 'X' => 0, 
            'B' | 'Y' => 1, 
            'C' | 'Z' => 2,
            _ => -1
        }).collect()).collect();
    // println!("{:?}", array);

    let scores: Vec<i32> = array.iter().map(
        // The score of the game is the value of whatever you played
        |single_game| match single_game {
            _ if single_game[1] == 0 => ((3 + single_game[0] - 1) % 3) + 1,  // lose
            _ if single_game[1] == 1 => single_game[0] + 4,  // draw
            _ if single_game[1] == 2 => 6 + (((single_game[0] + 1) % 3) + 1),  // win
            _ => 0
        }
    ).collect();

    // println!("{:?}", scores);

    Ok(scores.iter().sum())
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day2_1() {
        assert_eq!(day2_1("data/test2_1.txt").unwrap(), 15);
    }

    #[test]
    fn test_day2_1_bis() {
        assert_eq!(day2_1("data/test2_2.txt").unwrap(), 15);
    }

    #[test]
    fn test_day2_2() {
        assert_eq!(day2_2("data/test2_2.txt").unwrap(), 12);
    }
}