use std::io;

mod day1;
mod day2;
mod day3;
mod day4;
mod day5;
mod day6;
mod day7;
mod day8;
mod day9;
mod day10;
mod day11;
mod day12;
mod day13;
mod day14;

fn main() -> io::Result<()> {
    // let days = (1..9).collect::<Vec<i32>>();
    let days = vec![13];

    if days.contains(&1) {
        let total = day1::day1_1("data/input1_1.txt");
        println!("Day 1 Part 1: {}", total.unwrap());

        let total_2 = day1::day1_2("data/input1_1.txt");
        println!("Day 1 Part 2: {}", total_2.unwrap());
    }

    if days.contains(&2) {
        let total = day2::day2_1("data/input2_1.txt");
        println!("Day 2 Part 1: {}", total.unwrap());

        let total = day2::day2_2("data/input2_1.txt");
        println!("Day 2 Part 2: {}", total.unwrap());
    }

    if days.contains(&3) {
        let total = day3::day3_1(include_bytes!("../data/input3_1.txt"));
        println!("Day 3 Part 1: {}", total.unwrap());

        let total = day3::day3_2(include_bytes!("../data/input3_1.txt"));
        println!("Day 3 Part 1: {}", total.unwrap());
    }

    if days.contains(&4) {
        let total = day4::day4_1("data/input4_1.txt");
        println!("Day 4 Part 1: {}", total.unwrap());

        let total = day4::day4_2("data/input4_1.txt");
        println!("Day 4 Part 1: {}", total.unwrap());
    }

    if days.contains(&5) {
        let total = day5::day5_1(include_str!["../data/input5_1.txt"], false, 9);
        println!("Day 5 Part 1: {}", total.unwrap());

        let total = day5::day5_1(include_str!["../data/input5_1.txt"], true, 9);
        println!("Day 5 Part 1: {}", total.unwrap());
    }

    if days.contains(&6) {
        let total = day6::day6_1(include_str!["../data/input6_1.txt"], 4);
        println!("Day 6 Part 1: {}", total.unwrap());

        let total = day6::day6_1(include_str!["../data/input6_1.txt"], 14);
        println!("Day 6 Part 1: {}", total.unwrap());
    }

    if days.contains(&7) {
        let total = day7::day7_1("data/input7_1.txt");
        println!("Day 7 Part 1: {}", total.unwrap());

        let total = day7::day7_2("data/input7_1.txt");
        println!("Day 7 Part 1: {}", total.unwrap());
    }

    if days.contains(&8) {
        let total = day8::day8_1("data/input8_1.txt");
        println!("Day 8 Part 1: {}", total.unwrap());

        // 196 is too low, it was multiply you moron
        let total = day8::day8_2("data/input8_1.txt");
        println!("Day 8 Part 1: {}", total.unwrap());
    }

    if days.contains(&9) {
        // 8879, 8878 too high
        // 6091 too high too after fixing dedup
        // I added one to compensate for the origin, but ofc the rope passed the origin at some point in the 
        // larger input, so I counted it double. Fixed by adding origin before dedup
        let total = day9::day9_1("data/input9_1.txt");
        println!("Day 9 Part 1: {}", total.unwrap());

        let total = day9::day9_2("data/input9_1.txt");
        println!("Day 9 Part 1: {}", total.unwrap());
    }

    if days.contains(&10) {
        // 8879, 8878 too high
        // 6091 too high too after fixing dedup
        // I added one to compensate for the origin, but ofc the rope passed the origin at some point in the 
        // larger input, so I counted it double. Fixed by adding origin before dedup
        let total = day10::day10_1("data/input10_1.txt");
        println!("Day 10 Part 1: {}", total.unwrap());

        // let total = day9::day9_2("data/input9_1.txt");
        // println!("Day 9 Part 1: {}", total.unwrap());
    }

    if days.contains(&11) {
        let total = day11::day11_1("data/input11_1.txt", 20, true);
        println!("Day 11 Part 1: {}", total.unwrap());

        let total = day11::day11_1("data/input11_1.txt", 10000, false);
        println!("Day 11 Part 2: {}", total.unwrap());
    }

    if days.contains(&12) {
        let total = day12::day12_1("data/input12_1.txt");
        println!("Day 12 Part 1: {}", total.unwrap());

        let total = day12::day12_2("data/input12_1.txt");
        println!("Day 12 Part 2: {}", total.unwrap());
    }

    if days.contains(&13) {
        // 6911 too high
        // I did it in python :(
        // It literally took half an hour there...
        // let total = day13::day13_1("data/input13_1.txt");
        // println!("Day 13 Part 1: {}", total.unwrap());
    }

    Ok(())
}
