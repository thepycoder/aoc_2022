use std::io;

mod day1;
mod day2;

fn main() -> io::Result<()> {
    let day = 2;

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
    Ok(())
}
