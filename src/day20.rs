use std::{fs, collections::HashSet};

pub fn day20_1(filepath: &str) -> Result<i32, std::io::Error> {
    // Read the input file line by line
    let input_str: String = fs::read_to_string(filepath)?;
    // Format: [original value, original index, modified index]
    let original: Vec<i32> = input_str
        .split("\n")
        .map(|(e)| e.parse::<i32>().unwrap())
        .collect();
    let mut modified: Vec<*const i32> = original.iter().map(|f| f as *const i32).collect();
    let list_len = original.len();

    // dbg!(&original);
    // dbg!(&modified);

    for original_value in original.iter() {
        // Get the modified index of the original value'
        // let test: Vec<_> = modified.iter().map(|p| {dbg!(*p); dbg!(original_value as *const i32)}).collect();
        let modified_index = modified.iter().position(|r| *r == original_value as *const i32).unwrap();
        // dbg!(modified_index);
        modified.remove(modified_index);

        // Then re-insert at the new location
        let mut new_index = modified_index as i32 + original_value;
        // dbg!(new_index);
        new_index = new_index.rem_euclid(list_len as i32 - 1);
        // dbg!(new_index);
        modified.insert(new_index as usize, original_value as *const i32);
        // dbg!(&modified);
    }

    // Print resulting list values
    // dbg!(&modified);
    let mut zero_index = 0;
    for (i, pointer) in modified.iter().enumerate() {
        unsafe {
            // dbg!(**pointer);
            if **pointer == 0 {
                zero_index = i as i32;
            }
        }
    }

    dbg!(&zero_index);

    let mut answer = 0;
    for x in vec![1000, 2000, 3000] {
        let pointer = modified[(zero_index + x).rem_euclid(list_len as i32) as usize];
        unsafe {
            // dbg!(*pointer);
            answer += *pointer;
        }
    }

    Ok(answer)
}

pub fn day20_2(filepath: &str) -> Result<i64, std::io::Error> {
    // Read the input file line by line
    let input_str: String = fs::read_to_string(filepath)?;
    // Format: [original value, original index, modified index]
    let original: Vec<i64> = input_str
        .split("\n")
        .map(|(e)| e.parse::<i64>().unwrap() * 811589153)
        .collect();
    let mut modified: Vec<*const i64> = original.iter().map(|f| f as *const i64).collect();
    let list_len = original.len();

    // dbg!(&original);
    // dbg!(&modified);
    for _ in 0..10 {

        for original_value in original.iter() {
            // Get the modified index of the original value'
            // let test: Vec<_> = modified.iter().map(|p| {dbg!(*p); dbg!(original_value as *const i64)}).collect();
            let modified_index = modified.iter().position(|r| *r == original_value as *const i64).unwrap();
            // dbg!(modified_index);
            modified.remove(modified_index);

            // Then re-insert at the new location
            let mut new_index = modified_index as i64 + original_value;
            // dbg!(new_index);
            new_index = new_index.rem_euclid(list_len as i64 - 1);
            // dbg!(new_index);
            modified.insert(new_index as usize, original_value as *const i64);
            // dbg!(&modified);
        }

    }

    // Print resulting list values
    // dbg!(&modified);
    let mut zero_index = 0;
    for (i, pointer) in modified.iter().enumerate() {
        unsafe {
            // dbg!(**pointer);
            if **pointer == 0 {
                zero_index = i as i64;
            }
        }
    }

    dbg!(&zero_index);

    let mut answer = 0;
    for x in vec![1000, 2000, 3000] {
        let pointer = modified[(zero_index + x).rem_euclid(list_len as i64) as usize];
        unsafe {
            // dbg!(*pointer);
            answer += *pointer;
        }
    }

    Ok(answer)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day20_1() {
        assert_eq!(day20_1("data/test20_1.txt").unwrap(), 3);
    }

    #[test]
    fn test_day20_2() {
        assert_eq!(day20_2("data/test20_1.txt").unwrap(), 1623178306);
    }
}