## Raid Shadow Legends Summon Simulator
This essentially just simulates opening shards on Raid Shadow Legends.
I wrote it for fun

## Usage examples:
* `python simulator.py --ancient-shards 50 -2x` - open 50 ancient shards with 2x event rates

## Screenshots
![Example Useage](https://i.imgur.com/CXIS9dq.png)

## Mercy system:
* This works, just enter your mercy values in mercy.json. You can use RSL-helper to figure out your mercy values.
* Keep in mind, the order for mercy.json matters. You'll get bugs if you change the order of things. Only change the numbers.

## What if I want the numbers for a desired outcome or the averages?
Well, then just go [here](https://gist.github.com/JackofSpades707/5e9c9da9ba3c51e7f202dfa04696da74)
Essentially, during a 2x event, you want an average of 88 ancient shards to pull a legendary when taking the mercy system into account (based off 100_000 iterations of simulations).

## Why is this a Command-Line tool?
* I didn't want to spend more than a few hours until I had a fully working version, CLI's are fun, easy, and quick to write.
* I personally prefer CLI tools generally.
* The data/functionality being correct matters the most for this.

## Will this ever get a UI?
Probably not. Although I would like to hook into the games memory for a few things.

## Will this get any additional features?
Not sure. I mostly just wrote this for myself, and for fun. But anyone is welcome to use it.
I'd love to be able to get the data for determining which champion gets summoned.
If anyone has the data for that, I would love to collaborate with you, if I got that data, I may actually build a real UI for this.

I'd also like to hook into the games memory and read the amount of shards you have if no arguments are provided.
And read your mercy values.
That'd be convenient. But this is basically complete as-is.
