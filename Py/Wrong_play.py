#!/usr/bin/env python3

import sys
import chess
import chess.syzygy
import chess.engine
from chess.engine import Cp, Mate, MateGiven
import csv
from pathlib import Path


#get the move played by lc0 with different search budget
def get_lc0_move(board):

    '''move with search'''
   
    result_MCTS_400 = engine_MCTS_400.play(board, chess.engine.Limit(nodes=400)) #400
    result_MCTS_800 = engine_MCTS_800.play(board, chess.engine.Limit(nodes=800)) #400+400=800
    result_MCTS_1600 = engine_MCTS_1600.play(board, chess.engine.Limit(nodes=1600)) # 800+800 =1600
    

    '''move without search'''
    result_Policy = engine_Policy.play(board, chess.engine.Limit(nodes=1))
    

    return result_MCTS_400.move.uci(),result_MCTS_800.move.uci(),result_MCTS_1600.move.uci(),result_Policy.move.uci()
    #return result_Policy.move.uci()
    


#load a tablebase
def get_EGTB(filename):
    Filepath = "/samples/"+ filename +".csv"

    with open(Filepath, mode='r') as infile:
        reader = csv.reader(infile)
        i = next(reader)

        moves = {rows[0]:rows[1:7] for rows in reader}

        return moves
      


def main():
    filename = sys.argv[1]
    
    moves = get_EGTB(filename)

    Filepath_w = "/failing/" +filename + ".csv"
    


    write_file = open(Filepath_w , 'w') 
    wr = csv.writer(write_file, delimiter = ',')
    
    #write the positions with lc0 selected moves
    wr.writerow(['position','WDL','Policy_pred','MCTS_pred_400','MCTS_pred_800','MCTS_pred_1600','winning_moves','drawing_moves','loasing_moves','move_Policy','move_MCTS_400','move_MCTS_800','move_MCTS_1600'])


    for key, val in moves.items():
    
        winning_moves = val[0]
        loasing_moves = val[1]
        drawing_moves = val[2]
        best_moves = val[3]
        WLD = val[4]

        #assume wrong move selected initoally
        Policy_pred = 0
        MCTS_pred_400 = 0
        MCTS_pred_800 = 0
        MCTS_pred_1600 = 0



        board = chess.Board(key)
    
        if not ((board.is_stalemate()) or (board.is_checkmate())) and (board.legal_moves.count()>1):
            move_MCTS_400,move_MCTS_800,move_MCTS_1600,move_Policy = get_lc0_move(board)
            
            
            #winning position
            if (WLD == 'W'):
            
                #check if winning move is selected
                if move_Policy in winning_moves:
                    Policy_pred = 1
                if move_MCTS_400 in winning_moves:
                    MCTS_pred_400 = 1
                if move_MCTS_800 in winning_moves:
                    MCTS_pred_800 = 1
                if move_MCTS_1600 in winning_moves:
                    MCTS_pred_1600 = 1
                
                if (((Policy_pred==0)or(MCTS_pred_400==0)or(MCTS_pred_800==0)or(MCTS_pred_1600==0))and(WLD != 'L')):
                    wr.writerow([key,WLD,Policy_pred,MCTS_pred_400,MCTS_pred_800,MCTS_pred_1600,winning_moves,drawing_moves,loasing_moves,move_Policy,move_MCTS_400,move_MCTS_800,move_MCTS_1600])
                
            elif((WLD == 'D')and (len(loasing_moves)>2)):
            #check if drawing move is selected on drawing position with losing move

                if move_Policy in drawing_moves:
                    Policy_pred = 1

                if move_MCTS_400 in drawing_moves:
                    MCTS_pred_400 = 1
                if move_MCTS_800 in drawing_moves:
                    MCTS_pred_800 = 1
                if move_MCTS_1600 in drawing_moves:
                    MCTS_pred_1600 = 1
                
                if (((Policy_pred==0)or(MCTS_pred_400==0)or(MCTS_pred_800==0)or(MCTS_pred_1600==0))and(WLD != 'L')):
                    wr.writerow([key,WLD,Policy_pred,MCTS_pred_400,MCTS_pred_800,MCTS_pred_1600,winning_moves,drawing_moves,loasing_moves,move_Policy,move_MCTS_400,move_MCTS_800,move_MCTS_1600])


if __name__ == '__main__':
    'Lc0'
    'Lc0 start'
    engine_MCTS_400 = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")
    engine_MCTS_800 = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")
    engine_MCTS_1600 = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")
    engine_Policy = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")

    '''configure Lc0 settings'''
    engine_MCTS_400.configure({"WeightsFile":'/weights/J92-330',"SmartPruningFactor":0,"Threads":1})
    engine_MCTS_800.configure({"WeightsFile":'/weights/J92-330',"SmartPruningFactor":0,"Threads":1})
    engine_MCTS_1600.configure({"WeightsFile":'/weights/J92-330',"SmartPruningFactor":0,"Threads":1})
    engine_Policy.configure({"WeightsFile":'/weights/J92-330'})
    
    main()
    #quit Lc0
    engine_MCTS_400.quit()
    engine_MCTS_800.quit()
    engine_MCTS_1600.quit()
    engine_Policy.quit()
