import chess
import chess.syzygy
import chess.gaviota
import chess.pgn
import csv
import sys

from csv import writer
from csv import reader


syzygy_path = "/syzygy"
nalimov_path = "/Gaviota"
tablebase = chess.syzygy.open_tablebase(syzygy_path)
nalimov = chess.gaviota.open_tablebase(nalimov_path)
    



"""get the best losing move for drawing positions"""
def second_best_move(board):
    
    wdl = tablebase.probe_wdl(board)
    #print("checkmate:", board.is_checkmate(), ",stalemate:", board.is_stalemate(),",variant_win:",board.is_variant_win(),",variant_loss:",board.is_variant_loss(),",insufficient_material:",board.is_insufficient_material(),"wdl:",tablebase.probe_wdl(board),",dtz:",tablebase.probe_dtz(board),",dtm:", nalimov.probe_dtm(board),"moves:")
    loosing_moves = list()
    winning_moves = list()
    drawing_moves = list()
    best_move = list()
    best_loasing = list()
    
    
    if (wdl==0):
        second_best_dtm = 0
    for move in board.legal_moves:
        zeroing = board.is_zeroing(move)
        board.push(move)
        if (tablebase.probe_wdl(board)>0):
            loosing_moves.append(move.uci())
        else:
            drawing_moves.append(move.uci())

        if(nalimov.probe_dtm(board)>second_best_dtm):
            best_loasing = list({move.uci()})
            second_best_dtm = nalimov.probe_dtm(board)
        elif (nalimov.probe_dtm(board)==second_best_dtm):
            best_loasing.append(move.uci())

    
                   
            
        #print("uci:",move,",zeroing:",zeroing,",checkmate:", board.is_checkmate(), ",stalemate:", board.is_stalemate(),",variant_win:",board.is_variant_win(),",variant_loss:",board.is_variant_loss(),",insufficient_material:",board.is_insufficient_material(),"wdl:",tablebase.probe_wdl(board),",dtz:",tablebase.probe_dtz(board),",dtm:",nalimov.probe_dtm(board))
        board.pop()

    

    return best_loasing,second_best_dtm






def add_second_best(filename):
    read_file = 'samples/'+ filename +'_draw.csv'
    write_file = 'samples/'+ filename +'_draw_losing_dtm.csv'
    with open(read_file, 'r') as read_obj, \
        open(write_file, 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        
        i = next(csv_reader)
        i.append('best_loasing')
        i.append('second_best_dtm')
        csv_writer.writerow(i)
        #print(i)
        for row in csv_reader:
            board = chess.Board(row[0])
            best_loasing,second_best_dtm = second_best_move(board)
            row.append(best_loasing)
            row.append(second_best_dtm)
            csv_writer.writerow(row)



def main():
    filename = sys.argv[1]
    add_second_best(filename)

main()



