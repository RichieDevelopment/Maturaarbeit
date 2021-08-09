import os
from datetime import datetime as datetime
import torch
import torchinfo
from torchinfo import summary


class Statistik_PongO:
    def __init__(self, model=None, msg='', lr=0,bs=0,gamma=0, ms=0):
        self.learning_rate = lr
        self.batch_size = bs
        self.memory_size = ms
        self.gamma = gamma
        self.model = model
        self.score_schwellwert = 6
        self.msg = msg
        self.list_stat = []
        self.list_stat_counter = 1
        self.list_last_state = ''
        self.Namensgebung = True
        self.same_size = True
        self.list_stat = []
        self.list_stat_counter = 1
        self.dateTimeobj = datetime.now()
        self.dateString = str(self.dateTimeobj.day) + '%' + str(self.dateTimeobj.month) + '%' + str(self.dateTimeobj.year) + '&' + str(
        self.dateTimeobj.hour) + '%' + str(self.dateTimeobj.minute)
        self.dateString_writing = str(self.dateTimeobj.day) + '.' + str(self.dateTimeobj.month) + '.' + str(
        self.dateTimeobj.year) + '_' + str(
        self.dateTimeobj.hour) + ':' + str(self.dateTimeobj.minute)
        self.statistik_file = r'C:/Users/Richie/Downloads/Policy_Gradient_Raumschiff/Policy_Gradient_Raumschiff/PongO/Test_Resultate_1/statistik_Policy_Gradient.csv'
        self.new_statistik = True
        if os.path.isfile(self.statistik_file):
            self.new_statistik = False
            datei = open(self.statistik_file)
            for i in datei:
                self.list_stat.append(i.rstrip())
            datei.close()
            self.anzahl_spalten = self.list_stat[1].count(';') + 1


    def add(self, score):
        if self.new_statistik:
            if self.Namensgebung:
                dateTimeobj = datetime.now()
                self.dateString = str(dateTimeobj.day) + '%' + str(dateTimeobj.month) + '%' + str(
                    dateTimeobj.year) + '&' + str(
                    dateTimeobj.hour) + '%' + str(dateTimeobj.minute) + '_' + str(self.msg)
                self.list_stat.append(self.dateString)
                self.Namensgebung = False

            self.list_stat.append(str(score))
        else:
            if self.Namensgebung:
                dateTimeobj = datetime.now()
                self.dateString = str(dateTimeobj.day) + '%' + str(dateTimeobj.month) + '%' + str(
                    dateTimeobj.year) + '&' + str(
                    dateTimeobj.hour) + '%' + str(dateTimeobj.minute) + '_' + str(self.msg)
                self.list_stat[0] = self.list_stat[0] + ';' + self.dateString_writing + '_' + str(self.msg)
                self.Namensgebung = False

            if self.list_stat_counter + 1 < len(self.list_stat):
                if self.list_stat[self.list_stat_counter].count(';') >= self.list_stat[1].count(';') - 1:
                    self.list_stat[self.list_stat_counter] += (';' + str(score))
                else:
                    platzhalter_1 = self.list_stat[2].count(';') - 1 - self.list_stat[self.list_stat_counter].count(';')
                    self.list_stat[self.list_stat_counter] += ';'
                    for _ in range(platzhalter_1):
                        self.list_stat[self.list_stat_counter] += ' ;'
                    self.list_stat[self.list_stat_counter] += (str(score))

            else:
                self.list_stat.append(' ')
                platzhalter_2 = self.list_stat[2].count(';') - 1
                for _ in range(platzhalter_2):
                    self.list_stat[self.list_stat_counter] += '; '
                self.list_stat[self.list_stat_counter] += ';' + str(score)
            self.list_stat_counter += 1

    def end_model(self,max_score,eps_train):
        assert self.model
        model_params = summary(self.model, (1, 6), verbose=0)
        dateTimeobj2 = datetime.now()

        with open(f"C:/Users/Richie/Downloads/Policy_Gradient_Raumschiff/Policy_Gradient_Raumschiff/PongO/Test_Resultate_1/Modelle/Policy_Gradient_Model&{self.dateString}_{self.msg}.txt", 'w', encoding='utf-8') as f:
            f.write(model_params.__str__() + '\n')
            f.write(f'Maximal erreichte Schlaege: {max}\n')
            f.write(f'Maximal erreichter Score: {max_score}\n')
            f.write(f'Learning rate: {self.learning_rate}\n')
            f.write(f'Batch size: {self.batch_size}\n')
            f.write(f'Memory size: {self.memory_size}\n')
            f.write(f'Gamma: {self.gamma}\n')
            f.write(f'Trainierte Epochen: {eps_train}\n')
            f.write(f'Training beendet: {dateTimeobj2}\n')
            f.write(f'Trainingszeit: {dateTimeobj2 - self.dateTimeobj}\n')
        torch.save(self.model.state_dict(), f'C:/Users/Richie/Downloads/Policy_Gradient_Raumschiff/Policy_Gradient_Raumschiff/PongO/Test_Resultate_1/Gewichte/Policy_Gradient_Gewichte&{self.dateString}_{self.msg}.dat')

    def end_writing(self):
        datei = open(self.statistik_file, 'w')
        for i in self.list_stat:
            datei.write(i + "\n")
        datei.close()

