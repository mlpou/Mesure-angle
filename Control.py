import Ipano # type: ignore
import time

ipano = Ipano.IPANO('COM5')
ipano.set_zero_position()

def measures(altIterations, altPrecision,  azIterations, pauseTime) :
    ipano.goto((0-altIterations)*2, 0*(360/azIterations))
    time.sleep(7)
    for i in range(altIterations) :
        for j in range(azIterations) :
            time.sleep(pauseTime)
            ipano.goto((i-altIterations/2)*altPrecision, j*(360/azIterations))

measures(20, 2, 20, 2)