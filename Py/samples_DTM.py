import sys
import chess
import chess.gaviota
import chess.engine

from chess.engine import Cp, Mate, MateGiven
import time

from csv import writer
from csv import reader


tablebase = chess.gaviota.open_tablebase("/Gaviota")


def DTM(key):    
    board = chess.Board(key)
    return tablebase.probe_dtm(board)
    
  
def add_DTM(filename):
    read_file = '/samples/'+ filename +'_win.csv'
    write_file = '/samples/'+ filename +'win_dtm..csv'
    with open(read_file, 'r') as read_obj, \
        open(write_file, 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        i = next(csv_reader)       
        i.append('DTM')
        csv_writer.writerow(i)
        for row in csv_reader:
            row.append(DTM(row[0]))
            csv_writer.writerow(row)

    
def start():
    filename = sys.argv[1]
    add_DTM(filename)

start()   
