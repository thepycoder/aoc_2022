use core::panic;
use std::collections::HashSet;
use std::fs;
// use std::io;

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Coord {
    x: i32,
    y: i32
}

fn deduplicate(coordinates: Vec<Coord>) -> Vec<Coord> {
    let mut set = HashSet::new();
    let mut deduplicated = Vec::new();

    for coord in coordinates {
        // Only add the coordinate to the deduplicated vector if it is not already in the set
        if set.insert(coord) {
            deduplicated.push(coord);
        }
    }
    // dbg!(set.len());
    deduplicated
}

// fn display_grid(coordinates: &Vec<Coord>) -> io::Result<()> {

//     let size: i32 = 26;

//     // Create the grid and fill it with dots
//     let mut grid = vec![vec!['.'; (size + 1) as usize]; size as usize];

//     // Replace the dots at the coordinates in the vector with #
//     let mut nr: u8 = 0;
//     for coord in coordinates {
//         grid[(coord.y + 21) as usize][(coord.x + 12) as usize] = nr.to_string().chars().nth(0).unwrap();
//         nr += 1;
//         if nr == 10 {
//             nr = 0
//         }
//     }

//     // Print the grid
//     for row in grid {
//         for cell in row {
//             print!("{}", cell);
//         }
//         println!();
//     }
//     println!("=======");

//     Ok(())
// }


pub fn day9_1(filepath: &str) -> Result<usize, std::io::Error> {
    let input_str: String = fs::read_to_string(filepath)?;

    let mut head: Coord = Coord { x: 0, y: 0 };
    let mut last_head_position: Coord = Coord { x: 0, y: 0 };
    let mut tail: Coord = Coord { x: 0, y: 0 };

    let commands: Vec<Vec<&str>> = input_str.split("\n").map(|line| line.split(" ").collect::<Vec<&str>>()).collect();
    let mut result: Vec<Coord> = commands
        .iter()
        .map(|command| {
            let amount = command[1].parse::<i32>().unwrap();
            let mut tail_positions: Vec<Coord> = Vec::new();
            for _ in 0..amount {
                match command[0] {
                    "U" => head.y -= 1,
                    "D" => head.y += 1,
                    "L" => head.x -= 1,
                    "R" => head.x += 1,
                    _ => panic!("This should not happen!")
                }
                // dbg!(head);
                if !check_touching(head, tail) {
                    tail = last_head_position;
                    tail_positions.push(tail); // return tail so the map iterator can become a Vec<Coord> with the tail history in it.
                }
                last_head_position = head;
                // display_grid(&vec![head, tail]);
                // dbg!(head);
                // dbg!(tail);
                // println!("=====")
            }
            tail_positions
        })
        .flatten()
        .collect();
    result.push(Coord {x: 0, y: 0});

    // dbg!(&result);
    result = deduplicate(result);
    // display_grid(&result);
    // dbg!(&result);
    Ok(result.iter().count())
}

pub fn day9_2(filepath: &str) -> Result<usize, std::io::Error> {
    let input_str: String = fs::read_to_string(filepath)?;

    let mut tails: Vec<Coord> = vec![Coord { x: 0, y: 0 }; 10];
    let mut last_positions: Vec<Coord> = vec![Coord { x: 0, y: 0 }; 10];

    let commands: Vec<Vec<&str>> = input_str.split("\n").map(|line| line.split(" ").collect::<Vec<&str>>()).collect();
    let mut result: Vec<Coord> = commands
        .iter()
        .map(|command| {
            let amount = command[1].parse::<i32>().unwrap();
            let mut tail_positions: Vec<Coord> = Vec::new();
            let scope_tails: &mut Vec<Coord> = &mut tails;
            for _ in 0..amount {
                match command[0] {
                    "U" => scope_tails[0].y -= 1,
                    "D" => scope_tails[0].y += 1,
                    "L" => scope_tails[0].x -= 1,
                    "R" => scope_tails[0].x += 1,
                    _ => panic!("This should not happen!")
                }
                for i in 0..scope_tails.len() - 1 {
                    let new_tail_position = update_tail(scope_tails[i], scope_tails[i+1]);
                    last_positions[i+1] = scope_tails[i+1];
                    scope_tails[i+1] = new_tail_position;
                    if i == scope_tails.len() - 2 {
                        tail_positions.push(new_tail_position);
                    }
                }
                last_positions[0] = scope_tails[0];
            }
            tail_positions
        })
        .flatten()
        .collect();
    // result.truncate(&result.len() - 9);
    result.push(Coord {x: 0, y: 0});

    // dbg!(&result);
    result = deduplicate(result);
    // display_grid(&result);
    // dbg!(&result);
    Ok(result.iter().count())
}

fn update_tail(head: Coord, tail: Coord) -> Coord {
    if !check_touching(head, tail) {
        let x_diff = head.x - tail.x;
        let y_diff = head.y - tail.y;
        let mut new_position = tail;

        if x_diff > 0 {
            new_position.x += 1;
        } else if x_diff < 0 {
            new_position.x -= 1;
        }

        if y_diff > 0 {
            new_position.y += 1;
        } else if y_diff < 0 {
            new_position.y -= 1;
        }
        return new_position;
    }
    tail
}

fn check_touching(head: Coord, tail: Coord) -> bool {
    if (head.x - tail.x).abs() > 1 || (head.y - tail.y).abs() > 1 {
        return false;
    }
    true
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day9_1() {
        assert_eq!(day9_1("data/test9_1.txt").unwrap(), 13);
    }

    #[test]
    fn test_day9_2() {
        assert_eq!(day9_2("data/test9_2.txt").unwrap(), 36);
    }

    // #[test]
    // fn test_day9_2() {
    //     assert_eq!(day9_2("data/test9_1.txt").unwrap(), 24933642);
    // }
}