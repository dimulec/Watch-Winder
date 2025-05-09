import board
import digitalio
import analogio
import displayio
import time

m_ena = digitalio.DigitalInOut(board.A0)
m_ena.direction = digitalio.Direction.OUTPUT
m_ena.value = False

m_ms1 = digitalio.DigitalInOut(board.A1)
m_ms1.direction = digitalio.Direction.OUTPUT
m_ms1.value = True

m_ms2 = digitalio.DigitalInOut(board.A2)
m_ms2.direction = digitalio.Direction.OUTPUT
m_ms2.value = False

m_pdn = digitalio.DigitalInOut(board.A3)
m_pdn.direction = digitalio.Direction.OUTPUT
m_pdn.value = False

m_stp = digitalio.DigitalInOut(board.A4)
m_stp.direction = digitalio.Direction.OUTPUT

m_dir = digitalio.DigitalInOut(board.A5)
m_dir.direction = digitalio.Direction.OUTPUT

adc = analogio.AnalogIn(board.D9)

button0 = digitalio.DigitalInOut(board.D0)
button0.switch_to_input(pull=digitalio.Pull.UP)

button1 = digitalio.DigitalInOut(board.D1)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

m_stp.value = False
m_dir.value = True

counter = 0
turns = 5

sm_stop = 0
sm_left = 1
sm_right = 2
sm_both = 3

spinmode = sm_stop

display = board.DISPLAY
bitmap = displayio.OnDiskBitmap("/images/Stop.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

group = displayio.Group()
group.append(tile_grid)

main_group = displayio.Group()
main_group.append(group)

display.root_group = main_group

while True:
	if not button0.value:
		time.sleep(0.1)
		while not button0.value:
			pass
		time.sleep(0.1)
		if spinmode == sm_right:
			spinmode = sm_left
			m_dir.value = False
			tile_grid.bitmap = displayio.OnDiskBitmap("/images/Left.bmp")
		elif spinmode == sm_left:
			spinmode = sm_both
			tile_grid.bitmap = displayio.OnDiskBitmap("/images/Both.bmp")
		elif (spinmode == sm_both) or (spinmode == sm_stop):
			spinmode = sm_right
			m_dir.value = True
			tile_grid.bitmap = displayio.OnDiskBitmap("/images/Right.bmp")
		counter = 200

	if button1.value:
		time.sleep(0.1)
		while button1.value:
			pass
		time.sleep(0.1)
		spinmode = sm_stop
		tile_grid.bitmap = displayio.OnDiskBitmap("/images/Stop.bmp")
		counter = 0

	if (spinmode == sm_stop) and (counter > 0):
		time.sleep(0.1)
	else:
		m_stp.value = True
		time.sleep(0.0001)
		m_stp.value = False
		time.sleep(0.0001)
		if (counter > 0):
			counter = counter - 1
		if ((adc.value < 50000) and (counter == 0)):
			counter = 200
			if spinmode == sm_both:
				turns = turns - 1
			if (turns == 0):
				for i in range(1, 50):
					m_stp.value = True
					time.sleep(0.001)
					m_stp.value = False
					time.sleep(0.001)
				m_dir.value = not m_dir.value
				time.sleep(1)
				turns = 5
				for i in range(1, 50):
					m_stp.value = True
					time.sleep(0.001)
					m_stp.value = False
					time.sleep(0.001)
