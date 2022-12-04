use std::io;

mod day1;
mod day2;
mod day3;
mod day4;

fn main() -> io::Result<()> {
    let day = 4;

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
    Ok(())
}
