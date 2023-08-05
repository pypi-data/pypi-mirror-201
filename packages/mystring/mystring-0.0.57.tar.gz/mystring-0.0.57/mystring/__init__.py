import re
class string(str):
    def equals(self,*args):
        for arg in args:
            if self == arg:
                return True
        return False

    def replace(self,x,y):
        return string(super().replace(x,y))

    def rep(self,substring):
        self = self.replace(substring,'')
        return self

    def repsies(self,*args):
        for arg in args:
            self = self.rep(arg)
        return self

    @property
    def irregularstrip(self):
        #for arg in ['.','(',')','[',']','-',',','/','"',"'","’","#",]:
        #    self = self.rep(arg)
        self = string(re.sub(r'\W+', '', self))
        return self
    
    @property
    def deplete(self):
        self = self.trim.irregularstrip.trim
        if self.empty or self.equals("None", "none", "Null", "null", "NaN", "nan"):
            self = None
        return self

    def ad(self, value):
        self = string(self + getattr(self, 'delim', "")  + value)
        return self

    def delim(self, value):
        self.delim = value

    def pre(self, value):
        self = string(value + getattr(self, 'delim', "")  + self)
        return self

    def pres(self, *args):
        for arg in args:
            self = self.pre(arg)
        return self

    def startswiths(self, *args):
        for arg in args:
            if self.startswith(arg):
                return True
        return False

    @property
    def trim(self):
        self = string(self.strip())
        if self == '':
            self = None
        return self

    @property
    def empty(self):
        return self is None or self.strip() == '' or self.strip().lower() == 'nan' or self.strip().lower() == 'none'

    @property
    def notempty(self):
        return not self.empty

    def format(self, numstyle='06'):
        return format(int(self),numstyle)

    def splitsies(self,*args,joiner=":"):
        output_list = []
        for splitter_itr, splitter in enumerate(args):
            if splitter_itr == 0:
                output_list = self.split(splitter)
            else:
                temp_list = string(joiner.join(output_list)).splitsies(splitter,joiner=joiner)
                output_list = []
                for temp_item in temp_list:
                    for temp_split_item in temp_item.split(joiner):
                        output_list.append(temp_split_item)

        return output_list

    def tohash(self, hash_type='sha512', encoding='utf-8'):
        import hashlib
        return getattr(hashlib, hash_type)(self.encode(encoding)).hexdigest()

    def tobase64(self, encoding='utf-8'):
        import base64
        return base64.b64encode(self.encode(encoding)).decode(encoding)

    @staticmethod
    def frombase64(string, encoding='utf-8'):
        import base64
        return base64.b64decode(string.encode(encoding)).decode(encoding)

import pandas as pd
class frame(pd.DataFrame):
    def __init__(self,*args,**kwargs):
        super(frame,self).__init__(*args,**kwargs)

    def col_exists(self,column):
        return column in self.columns

    def col_no_exists(self,column):
        return not(self.col_exists(column))

    def column_decimal_to_percent(self,column):
        self[column] = round(round(
            (self[column]),2
        ) * 100,0).astype(int).astype(str).replace('.0','') + "%"
        return self

    def move_column(self, column, position):
        if self.col_no_exists(column):
            return
        colz = [col for col in self.columns if col != column]
        colz.insert(position, column)
        self = frame(self[colz])
        return self

    def rename_column(self, columnfrom, columnto):
        if self.col_no_exists(columnfrom):
            return
        self.rename(columns={columnfrom: columnto},inplace=True)
        return self

    def rename_columns(self, dyct):
        for key,value in dyct.items():
            if self.col_exists(key):
                self.rename(columns={key: value},inplace=True)
        return self

    def rename_value_in_column(self, column, fromname, fromto):
        if self.col_no_exists(column):
            return
        self[column] = self[column].str.replace(fromname, fromto)
        return self

    def drop_value_in_column(self, column, value,isstring=True):
        if self.col_no_exists(column):
            return
        self = frame(self.query("{0} != {1}".format(column, 
            "'" + value + "'" if isstring else value
        )))
        return self

    def cast_column(self, column, klass):
        if self.col_no_exists(column):
            return
        self[column] = self[column].astype(klass)
        return self
 
    def search(self, string):
        return frame(self.query(string))
 
    def arr(self):
        self_arr = self.to_dict('records')
        return self_arr

    def add_confusion_matrix(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN', use_percent:bool=False):
        prep = lambda x:frame.percent(x, 100) if use_percent else x

        self['Precision_PPV'] = prep(self[TP]/(self[TP]+self[FP]))
        self['Recall'] = prep(self[TP]/(self[TP]+self[FN]))
        self['Specificity_TNR'] = prep(self[TN]/(self[TN]+self[FP]))
        self['FNR'] = prep(self[FN]/(self[FN]+self[TP]))
        self['FPR'] = prep(self[FP]/(self[FP]+self[TN]))
        self['FDR'] = prep(self[FP]/(self[FP]+self[TP]))
        self['FOR'] = prep(self[FN]/(self[FN]+self[TN]))
        self['TS'] = prep(self[TP]/(self[TP]+self[FP]+self[FN]))
        self['Accuracy'] = prep((self[TP]+self[TN])/(self[TP]+self[FP]+self[TN]+self[FN]))
        self['PPCR'] = prep((self[TP]+self[FP])/(self[TP]+self[FP]+self[TN]+self[FN]))
        self['F1'] = prep(2 * ((self['Precision_PPV'] * self['Recall'])/(self['Precision_PPV'] + self['Recall'])))

        return self
    
    def confusion_matrix_sum(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
        return (self[TP].sum() + self[TN].sum() + self[FN].sum())  

    def verify_confusion_matrix_bool(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
        return len(self.arr()) == self.confusion_matrix_sum(TP=TP,FP=FP,TN=TN,FN=FN)

    def verify_confusion_matrix(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
        return "Total Cases {0} sum(TP,TN,FN)".format(
            "===" if self.verify_confusion_matrix_bool(TP=TP,FP=FP,TN=TN,FN=FN) else "=/="
        ) 

    @staticmethod
    def percent(x,y):
        return ("{0:.2f}").format(100 * (x / float(y)))

    @staticmethod
    def from_json(string):
        return frame(pd.read_json(string))

    @staticmethod
    def from_arr(arr):
        def dictionaries_to_pandas_helper(raw_dyct,deepcopy:bool=True):
            from copy import deepcopy as dc
            dyct = dc(raw_dyct) if deepcopy else raw_dyct
            for key in list(raw_dyct.keys()):
                dyct[key] = [dyct[key]]
            return pd.DataFrame.from_dict(dyct)

        return frame(
            pd.concat( list(map( dictionaries_to_pandas_helper,arr )), ignore_index=True )
        )

    @property
    def roll(self):
        class SubSeries(pd.Series):
            def setindexdata(self, index, data):
                self.custom__index = index
                self.custom__data = data
                return self

            def __setitem__(self, key, value):
                super(SubSeries, self).__setitem__(key, value)
                self.custom__data.at[self.custom__index,key] = value

        self.current_index=0
        while self.current_index < self.shape[0]:
            x = SubSeries(self.iloc[self.current_index]).setindexdata(self.current_index, self)

            self.current_index += 1
            yield x

    def tobase64(self, encoding='utf-8'):
        import base64
        return base64.b64encode(self.to_json().encode(encoding)).decode(encoding)

    @staticmethod
    def frombase64(string, encoding='utf-8'):
        import base64
        return frame.from_json(base64.b64decode(string.encode(encoding)).decode(encoding))
    
    def quick_heatmap(self,cmap ='viridis',properties={'font-size': '20px'}):
        return self.style.background_gradient(cmap=cmap).set_properties(**properties) 

    def heatmap(self, columns,x_label='',y_label='',title=''):
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set()
        SMALL_SIZE = 15
        MEDIUM_SIZE = 20
        BIGGER_SIZE = 25

        plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

        temp_frame = self.copy()
        mask = temp_frame.columns.isin(columns)

        temp_frame.loc[:, ~mask] = 0
        vmin, vmax = 0,0

        for col in columns:
            vmax = max(vmax, self[col].max())

        sns.heatmap(temp_frame, annot=True, fmt="d", vmin=vmin, vmax=vmax, cmap="Blues")
        plt.xlabel(x_label) 
        plt.ylabel(y_label) 

        # displaying the title
        plt.title(title)
        plt.rcParams["figure.figsize"] = (40,30)

        if False:
            plt.savefig(
                'get_size.png',
                format='png',
                dpi=height/fig.get_size_inches()[1]
            )
        plt.show()
    
    @property
    def df(self):
        from copy import deepcopy as dc
        return pd.DataFrame(dc(self))
    
    def dup(self):
        from copy import deepcopy as dc
        return frame(dc(self))
    
    @staticmethod
    def dupof(dataframe):
        from copy import deepcopy as dc
        return frame(dc(dataframe))
    
    @property
    def dummies(self):
        return pd.get_dummies(data = self)
    
    @property
    def kolz(self):
        return lyst(self.columns.tolist())


class lyst(list):
    def __init__(self,*args,**kwargs):
        super(lyst,self).__init__(*args,**kwargs)
    
    def trims(self, filterlambda=None):
        to_drop = []

        for x_itr,x in enumerate(self):
            if(
                (filterlambda != None and filterlambda(x))
                or
                (filterlambda == None and x == None)
            ):
                to_drop += [x_itr]
        
        to_drop.reverse()
        for to_drop_itr in to_drop:
            self.pop(to_drop_itr)
        
        return self
    
    @property
    def length(self):
        return len(self)

    def roll(self, kast=None,filter_lambda = None):
        for item in self:
            if kast:
                item = kast(item)

            if filter_lambda==None or filter_lambda(item):
                yield item
