## Synopsis
This is an example program using Gulf Coast Data Concept's SSP-x accelerometers. The python script reads incoming data from
a serial port and creates a live graph showing the frequency the accelerometer is vibrating at.

## Usage
In the terminal:  
`$ python grapherWithAnimation.py <Serial Port> <Chunk Size>`  
`<Chunk Size>` is the amount of data fetched at one time.
The default value is 150. A larger value will give more accurate graphs but slower animation

## Example
The accelerometer is taped to a subwoofer emitting a pitch at 77 hertz.
![graph](https://github.com/Awalrod/FrequencyPlotter/blob/master/figure_1.png)
