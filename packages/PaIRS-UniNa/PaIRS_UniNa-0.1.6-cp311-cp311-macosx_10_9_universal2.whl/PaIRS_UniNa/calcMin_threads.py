from .PaIRS_pypacks import*

class MINpar:
    def __init__(self):
        self.path=''
        self.list_Image_Files=[]
        self.list_eim=[]
        self.list_pim=[]
        self.flag_TR=None
        self.i=-1
        self.NumThreads=-1
        self.Imin=[np.array([]),np.array([])]
        self.initFlag=[True, True]
        self.nimg_proc=-1

    def duplicate(self):
        newist=MINpar()
        for f,v in self.__dict__.items():
            setattr(newist,f,copy.deepcopy(v))
        return newist
        
class calcMin_Signals(QObject):
    progress = Signal(int,int,list,bool,str)
    result = Signal(int,list,bool,int)
    completed = Signal()
    kill = Signal()
    error = Signal()

class calcMin_Worker(QRunnable):
    def __init__(self,par=MINpar,indWorker=int,indProc=int):
        super(calcMin_Worker,self).__init__(par,indWorker,indProc)
        self.nameWorker='calcMin_Worker'
        self.par=par.duplicate()
        
        self.signals=calcMin_Signals()
        self.isKilled = False
        self.indWorker = indWorker
        self.indProc = indProc

        #parameters which are not updated can be put in self instead of self.par
        self.nimg_tot=len(self.par.list_Image_Files)
        self.icont=0

    def run(self):
        try:
            while self.indWorker!=self.indProc and not self.isKilled:
                time.sleep(SleepTime_Workers)
            myprint(f'\nBeginning of Minimum Worker ({self.indWorker})')
            self.calcmin()
        except:
            myprint('\n!!! error from calcMin_Worker')
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            if self.isKilled: 
                myprint('\ncalcMin_Worker: I was killed!')
                self.signals.result.emit(self.icont,self.par.Imin,self.par.flag_TR,self.par.nimg_proc)
            else:
                myprint(f'\End of Minimum Worker ({self.indWorker}.{self.par.i}, {self.icont} read) ')
                self.signals.completed.emit()

    def calcmin(self):
        if self.par.flag_TR: di=2*self.par.NumThreads
        else: di=self.par.NumThreads
        
        i=self.par.i
        while i<self.nimg_tot:
            if self.isKilled:
                self.signals.kill.emit()
                return     
            if not self.par.list_pim[i]:
                if self.par.list_eim[i]:
                    j=i%2
                    try:
                        nameim=self.par.path+self.par.list_Image_Files[i]
                        I2=np.array(Image.open(nameim))
                        if self.par.initFlag[j]:
                            self.par.Imin[j]=I2
                            self.par.initFlag[j]=False
                        else:
                            
                            self.par.Imin[j]=np.minimum(self.par.Imin[j],I2)
                            if self.isKilled:
                                self.signals.kill.emit()
                                return  
                        self.par.list_pim[i]=1
                    except:
                        self.par.list_pim[i]=-1
                self.signals.progress.emit(i,self.par.list_pim[i],self.par.Imin,self.par.flag_TR,nameim+'\n')
                self.icont+=1
            if i==self.nimg_tot-2 and self.par.flag_TR:
                i=self.nimg_tot-1
            else:
                i+=di

    def die(self):
        self.isKilled = True

    @Slot(int)
    def updateIndProc(self,indProc):
        self.indProc=indProc