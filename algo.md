# algorithm


## distance - 1
```python
    power = (abs(rssi)- A)/(10.0 * n)
    distance = math.pow(10, power)
```
## distance - 2
```javascript
// Based on http://stackoverflow.com/a/20434019

function calculateAccuracy(txPower, rssi) {
  if (rssi === 0) {
    return -1; // if we cannot determine accuracy, return -1.
  }

  var ratio = rssi * 1 / txPower;
  if (ratio < 1.0) {
    return Math.pow(ratio, 10);
  } else {
    return (0.89976) * Math.pow(ratio, 7.7095) + 0.111;
  }
}
```

## distance -3
* link https://stackoverflow.com/questions/54650509/stabilize-rssi-on-ibeacons
* algo
```code
distance = 10^((rssi at 1m - rssi)/20)

distance = rssi *fiterFactor + oldDistance *(1 - FilterFactor)
```