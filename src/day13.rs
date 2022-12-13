use std::{fs, iter::zip};


pub fn day13_1(filepath: &str) -> Result<i32, std::io::Error> {
    let input_str: String = fs::read_to_string(filepath)?;

    let result: Vec<i32> = input_str
        .split("\n\n")
        .map(|pair_of_packets| {
            let single_packets: Vec<Vec<&str>> = pair_of_packets.split("\n").map(|single_packet| single_packet.split(",").collect()).collect();
            dbg!("=====");
            dbg!(&single_packets);
            let mut correct_order: i32 = -1;
            for (raw_char1, raw_char2) in zip(&single_packets[0], &single_packets[1]) {
                let clean_char1 = raw_char1.replace("[", "").replace("]", "");
                let clean_char2 = raw_char2.replace("[", "").replace("]", "");
                let char1 = clean_char1.as_str();
                let char2 = clean_char2.as_str();
                dbg!(&char1, &char2);
                // Catch empty brackets cases
                if char1.is_empty() && !char2.is_empty() {
                    correct_order = 1;
                    break;
                }
                if !char2.is_empty() && char2.is_empty() {
                    correct_order = 0;
                    break;
                }
                if char2.is_empty() && char2.is_empty() {
                    if raw_char1.len() < raw_char2.len() {
                        correct_order = 1;
                        break;
                    }
                    if raw_char1.len() > raw_char2.len() {
                        correct_order = 0;
                        break;
                    }
                    if single_packets[0].len() < single_packets[1].len() {
                        correct_order = 1;
                        break;
                    } else {
                        correct_order = 0;
                        break;
                    }
                }

                // All other cases
                let nr1 = char1.parse::<i32>().unwrap();
                let nr2 = char2.parse::<i32>().unwrap();

                if nr1 < nr2 {
                    correct_order = 1;
                    break;
                } else if nr1 > nr2 {
                    correct_order = 0;
                    break;
                }
            }
            if correct_order == -1 {
                if single_packets[0].len() < single_packets[1].len() {
                    correct_order = 1;
                } else {
                    correct_order = 0;
                }
            }
            correct_order
        })
        .collect::<Vec<i32>>();

    dbg!(&result);
    let mut answer = 0;
    for (i, v) in result.iter().enumerate() {
        if v == &1 {
            answer += (i + 1) as i32;
        }
    }
    Ok(answer)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day13_1() {
        assert_eq!(day13_1("data/test13_1.txt").unwrap(), 13);
    }

    #[test]
    fn test_day13_1_biss() {
        assert_eq!(day13_1("data/test13_2.txt").unwrap(), 1);
    }
}


// use std::str::FromStr;

// fn parse_string_to_vector<T: FromStr>(input: &str) -> Result<Vec<T>, T::Err> {
//     // Remove the outer square brackets from the input string
//     let input = &input[1..input.len()-1];

//     // Split the input string on the comma character to get a vector of string slices
//     let mut items = input.split(",");

//     // Initialize an empty vector to hold the parsed values
//     let mut vec = Vec::new();

//     // Loop through the items in the input string
//     while let Some(item) = items.next() {
//         // Check if the current item starts and ends with square brackets, indicating a nested vector
//         if item.starts_with("[") && item.ends_with("]") {
//             // Recursively parse the nested vector
//             let nested_vec = parse_string_to_vector(item)?;
//             vec.push(nested_vec);
//         } else {
//             // Parse the current item as a value of the specified type
//             let value = item.parse()?;
//             vec.push(value);
//         }
//     }

//     Ok(vec)
// }

// // Test the function with the example input string
// let input = "[1,[2,[3,[4,[5,6,7]]]],8,9]";
// let result = parse_string_to_vector::<i32>(input);
// assert_eq!(result, );
