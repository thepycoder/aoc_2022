/* ChatGPT prompt to automate the boring stuff
This only generated the input parser


Write a Rust function that is called "monkey_turn"
that takes these arguments:
- a vec of u32 called starting items
- an string called operation (can be +, -, * or /)
- a number called operation_value
- a number called test_divisible
- a number called if_true
- a number called if_false
Then write a parser that takes a text file containing
blocks of text like this:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0
...

and parses each block into the variables necessary to
feed to "monkey_turn".

*/

use regex::Regex;
use std::{fs, thread::current};

#[derive(Debug)]
struct Monkey {
    id: u32,
    items: Vec<u32>,
    operation: String,
    operation_value: String,
    test_divisible: u32,
    if_true: u32,
    if_false: u32,
    items_checked: u32
}


pub fn day11_1(filepath: &str, part_one: bool) -> Result<u32, std::io::Error> {
    // Define the regular expression for matching the blocks of text
    let re = Regex::new(r"(?mx)^Monkey\s(\d+):\s+
        Starting\sitems:\s+
        (\d+(?:\s*,\s*\d+)*)\s+
        Operation:\s+new\s*=\s*old\s*([+*])\s*(\d+|old)\s+
        Test:\s+divisible\s+by\s+(\d+)\s+
        If\strue:\s+throw\s+to\s+monkey\s+(\d+)\s+
        If\sfalse:\s+throw\s+to\s+monkey\s+(\d+)").unwrap();

    // Read the input file line by line
    let input_str: String = fs::read_to_string(filepath)?;

    let mut monkies : Vec<Monkey> = vec![];

    for line in input_str.split("\n\n") {
        dbg!(line);
        // Match each line against the regular expression
        let captures = re.captures(line).unwrap();

        // Extract the values for the function arguments
        let monkey_id = captures[1].parse::<u32>().unwrap();
        let starting_items = captures[2]
            .split(", ")
            .map(|s| s.parse::<u32>().unwrap())
            .collect::<Vec<u32>>();
        let operation = &captures[3];
        let operation_value = &captures[4];
        let test_divisible = captures[5].parse::<u32>().unwrap();
        let if_true = captures[6].parse::<u32>().unwrap();
        let if_false = captures[7].parse::<u32>().unwrap();

        let monkey = Monkey {
            id: monkey_id,
            items: starting_items,
            operation: operation.to_string(),
            operation_value: operation_value.to_string(),
            test_divisible,
            if_true,
            if_false,
            items_checked:0
        };

        &monkies.push(monkey);

        // Call the monkey_turn function and print the result
        // let target_monkey = monkey_turn(starting_items, operation, operation_value, test_divisible, if_true, if_false);
        // println!("Monkey {}: throwing to monkey {}", monkey_id, target_monkey);
    }


    let monkies_len = monkies.len();
    for _ in 0..20 {
        for monkey_id in 0..monkies_len {
            let current_monkies = &mut monkies;
            let current_monkey = &mut current_monkies.get_mut(monkey_id).unwrap();
            dbg!(&monkey_id);
            let mut to_move: Vec<_> = Vec::new();
            for _ in 0..current_monkey.items.len() {
                dbg!(&current_monkey.items);
                let current_monkey_items = &current_monkey.items;
                let worry_level = current_monkey_items.get(0).unwrap();
                current_monkey.items_checked += 1;
                dbg!(worry_level);
                let mut new_worry_level: u32;
                if current_monkey.operation_value == "old" {
                    new_worry_level = worry_level.pow(2);
                } else {
                    let operation_value_nr = current_monkey.operation_value.parse::<u32>().unwrap();
                    new_worry_level = match current_monkey.operation.as_str() {
                        "+" => *worry_level + operation_value_nr,
                        "-" => *worry_level - operation_value_nr,
                        "*" => *worry_level * operation_value_nr,
                        "/" => *worry_level / operation_value_nr,
                        _ => panic!("euh"),
                    };
                }
                if part_one {
                    new_worry_level = new_worry_level / 3;
                }

                dbg!(&new_worry_level);

                let new_monkey_id;
                if new_worry_level % current_monkey.test_divisible == 0 {
                    new_monkey_id = current_monkey.if_true;
                } else {
                    new_monkey_id = current_monkey.if_false;
                }

                current_monkey.items.remove(0);
                to_move.push((monkey_id, new_monkey_id, new_worry_level));

                // monkies[new_monkey_id as usize].items.push(new_worry_level);

            }

            for (from_id, to_id, value) in to_move {
                let new_monkey = &mut current_monkies.get_mut(to_id as usize).unwrap();
                new_monkey.items.push(value);
            }

        }
    }

    let mut monkey_business: Vec<u32> = Vec::new();
    for m in monkies {
        println!("Monkey: {}", m.id);
        println!("Times Checked: {}", m.items_checked);
        monkey_business.push(m.items_checked);
    }
    monkey_business.sort_by(|a, b| b.cmp(a));
    let answer = monkey_business[0] * monkey_business[1];


    Ok(answer)

}

// fn monkey_turn(starting_items: VecDeque<u32>, operation: &str, operation_value: &str, test_divisible: u32, if_true: u32, if_false: u32) -> u32 {
//     let mut new_items = Vec::new();
//     let mut new_worry_level: u32;
//     for worry_level in starting_items {
        
//     }

//     let mut target_monkey = if_false;
//     for item in new_items {
//         if item % test_divisible == 0 {
//             target_monkey = if_true;
//             break;
//         }
//     }

//     target_monkey
// }


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day11_1() {
        assert_eq!(day11_1("data/test11_1.txt", true).unwrap(), 10605);
    }

    #[test]
    fn test_day11_2() {
        assert_eq!(day11_1("data/test11_1.txt", false).unwrap(), 2713310158);
    }
}

