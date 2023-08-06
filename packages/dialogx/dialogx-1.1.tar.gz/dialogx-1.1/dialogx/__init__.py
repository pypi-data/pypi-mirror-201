"""DialogX, by MySoft
	Version 1.0"""

import sys
import os
sys.stdout = open(os.devnull, "w")
import pygame
sys.stdout = sys.__stdout__
del globals()["sys"]
print(__doc__)
import pygame.draw
import pygame.font
pygame.font.init()
import threading

def getUIFont(size):
	return pygame.font.SysFont("Verdana", size)

def new(typeStr, sizeTup, title="DialogX"):
	defPos = None
	fonts = {"title": getUIFont(16), "contents": getUIFont(12)}
	if typeStr == "surf":
		def blendCol(startCol, endCol, midpnts):
			startR = int(startCol[1:3], 16)
			startG = int(startCol[3:5], 16)
			startB = int(startCol[5:7], 16)
			endR = int(endCol[1:3], 16)
			endG = int(endCol[3:5], 16)
			endB = int(endCol[5:7], 16)
			stepR = (endR - startR) / (midpnts + 1)
			stepG = (endG - startG) / (midpnts + 1)
			stepB = (endB - startB) / (midpnts + 1)
			colors = [startCol]
			count = 1
			while count < midpnts + 1:
				r = round(startR + count * stepR)
				g = round(startG + count * stepG)
				b = round(startB + count * stepB)
				colors.append("#" + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2))
				count += 1
			colors.append(endCol)
			return colors

		def startWin():
			win = pygame.display.set_mode((sizeTup[0] + 16, sizeTup[1] + 71), pygame.NOFRAME)
			pygame.display.set_caption(title)
			running = True
			from dialogx.ctrlIcons import closeBtn, minimBtn
			drag = {"iniPos": None, "winPos": (100, 100)}
			import pygame._sdl2.video as sdlVid
			sdlVid.Window.from_display_module().position = drag["winPos"]
			while running:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
					elif event.type == pygame.MOUSEBUTTONDOWN:
						mousePos = event.pos
						if mousePos[1] < 17 and mousePos[0] > sizeTup[0] - 11 and mousePos[0] < sizeTup[0] + 8:
							running = False
						elif mousePos[1] < 17 and mousePos[0] > sizeTup[0] - 37 and mousePos[0] < sizeTup[0] - 18:
							pygame.display.iconify()
						elif mousePos[1] < 27 and drag["iniPos"] == None:
							drag["iniPos"] = mousePos
					elif event.type == pygame.MOUSEBUTTONUP:
						drag["iniPos"] = None
					elif event.type == pygame.MOUSEMOTION and drag["iniPos"] != None:
						mousePos = event.pos
						drag["winPos"] = list(drag["winPos"])
						drag["winPos"][0] += mousePos[0] - drag["iniPos"][0]
						drag["winPos"][1] += mousePos[1] - drag["iniPos"][1]
						drag["winPos"] = tuple(drag["winPos"])
				sdlVid.Window.from_display_module().position = drag["winPos"]
				win.fill("#eeeeee")
				win.blit(surf, (8, 36))
				gradCount = 0
				for col in blendCol("#bfbfbf", "#eeeeee", 25):
					pygame.draw.line(win, col, (0, gradCount), (sizeTup[0] + 16, gradCount))
					gradCount += 1
				win.blit(fonts["title"].render(title, True, "Black"), (4, 2))
				pygame.draw.line(win, "Black", (sizeTup[0] - 10, 0), (sizeTup[0] - 10, 15))
				pygame.draw.line(win, "Black", (sizeTup[0] - 9, 16), (sizeTup[0] + 6, 16))
				pygame.draw.line(win, "Black", (sizeTup[0] + 7, 0), (sizeTup[0] + 7, 15))
				gradCount = 0
				for col in blendCol("#8090ff", "#4060ff", 14):
					pygame.draw.line(win, col, (sizeTup[0] - 9, gradCount), (sizeTup[0] + 6, gradCount))
					charCount = 0
					for char in list(closeBtn[gradCount]):
						if char == "#":
							pygame.draw.line(win, "White", (sizeTup[0] - 9 + charCount, gradCount), (sizeTup[0] - 9 + charCount, gradCount))
						charCount += 1
					gradCount += 1
				pygame.draw.line(win, "Black", (sizeTup[0] - 36, 0), (sizeTup[0] - 36, 15))
				pygame.draw.line(win, "Black", (sizeTup[0] - 35, 16), (sizeTup[0] - 20, 16))
				pygame.draw.line(win, "Black", (sizeTup[0] - 19, 0), (sizeTup[0] - 19, 15))
				gradCount = 0
				for col in blendCol("#8090ff", "#4060ff", 14):
					pygame.draw.line(win, col, (sizeTup[0] - 35, gradCount), (sizeTup[0] - 20, gradCount))
					charCount = 0
					for char in list(minimBtn[gradCount]):
						if char == "#":
							pygame.draw.line(win, "White", (sizeTup[0] - 35 + charCount, gradCount), (sizeTup[0] - 35 + charCount, gradCount))
						charCount += 1
					gradCount += 1
				gradCount = 0
				for col in blendCol("#eeeeee", "#bfbfbf", 25):
					pygame.draw.line(win, col, (0, sizeTup[1] + 44 + gradCount), (sizeTup[0] + 16, sizeTup[1] + 44 + gradCount))
					gradCount += 1
				pygame.display.update()
		surf = pygame.Surface(sizeTup, pygame.NOFRAME)
		surf.fill("White")
		threading.Thread(target=startWin).start()
		return surf
	else:
		raise TypeError("Invalid typeStr '" + typeStr + "'")