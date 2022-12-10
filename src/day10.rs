use std::fs;


pub fn day10_1(filepath:  &str) -> Result<i32, std::io::Error> {

    let input_str: String = fs::read_to_string(filepath)?;
    let instructions: Vec<&str> = input_str.split("\n").collect();

    let mut instructions_vec: Vec<Vec<&str>> = instructions
        .iter()
        .map(|instruction| instruction.split(" ").collect::<Vec<&str>>())
        .collect();
    
    let mut cycles: i32 = 1;
    let mut register: i32 = 1;
    let mut trigger: i32 = 20;
    let mut signal_strength: Vec<i32> = Vec::new();
    

    for instruction in instructions_vec.iter() {
        let mut loops = 0;
        let mut buffer: i32 =  0;

        match instruction[0].trim() {
            "noop" => {
                loops = 1;
            },
            "addx" => {
                buffer = instruction[1].parse::<i32>().unwrap();
                loops = 2;
            }
            _ => panic!("Should not happen")
        }

        for _ in 0..loops {
            if cycles == trigger {
                signal_strength.push(cycles * register);
                trigger += 40;
            }
            cycles += 1;
        }

        register += buffer;


    }

    dbg!(&signal_strength);

    Ok(signal_strength.iter().sum())
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day10_1() {
        assert_eq!(day10_1("data/test10_1.txt").unwrap(), 13140);
    }

    #[test]
    fn test_day10_1_bis() {
        assert_eq!(day10_1("data/test10_2.txt").unwrap(), 13140);
    }

    // #[test]
    // fn test_day10_2() {
    //     assert_eq!(day10_1(include_str!["../data/test5_1.txt"], true, 3).unwrap(), "MCD");
    // }
}