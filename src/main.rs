use std::io;

mod day1;
mod day2;
mod day3;
mod day4;
mod day5;
mod day6;
mod day7;
mod day8;

fn main() -> io::Result<()> {
    let day = 8;

    if day == 1 {
        let total = day1::day1_1("data/input1_1.txt");
        println!("Final total: {}", total.unwrap());

        let total_2 = day1::day1_2("data/input1_1.txt");
        println!("{}", total_2.unwrap());
    }

    if day == 2 {
        let total = day2::day2_1("data/input2_1.txt");
        println!("{}", total.unwrap());

        let total = day2::day2_2("data/input2_1.txt");
        println!("{}", total.unwrap());
    }

    if day == 3 {
        let total = day3::day3_1(include_bytes!("../data/input3_1.txt"));
        println!("{}", total.unwrap());

        let total = day3::day3_2(include_bytes!("../data/input3_1.txt"));
        println!("{}", total.unwrap());
    }

    if day == 4 {
        let total = day4::day4_1("data/input4_1.txt");
        println!("{}", total.unwrap());

        let total = day4::day4_2("data/input4_1.txt");
        println!("{}", total.unwrap());
    }

    if day == 5 {
        let total = day5::day5_1(include_str!["../data/input5_1.txt"], false);
        println!("{}", total.unwrap());

        let total = day5::day5_1(include_str!["../data/input5_1.txt"], true);
        println!("{}", total.unwrap());
    }

    if day == 6 {
        let total = day6::day6_1(include_str!["../data/input6_1.txt"], 4);
        println!("{}", total.unwrap());

        let total = day6::day6_1(include_str!["../data/input6_1.txt"], 14);
        println!("{}", total.unwrap());
    }

    if day == 7 {
        let total = day7::day7_1("data/input7_1.txt");
        println!("{}", total.unwrap());

        let total = day7::day7_2("data/input7_1.txt");
        println!("{}", total.unwrap());
    }

    if day == 8 {
        let total = day8::day8_1("data/input8_1.txt");
        println!("{}", total.unwrap());

        // 196 is too low, it was multiply you moron
        let total = day8::day8_2("data/input8_1.txt");
        println!("{}", total.unwrap());
    }
    Ok(())
}
