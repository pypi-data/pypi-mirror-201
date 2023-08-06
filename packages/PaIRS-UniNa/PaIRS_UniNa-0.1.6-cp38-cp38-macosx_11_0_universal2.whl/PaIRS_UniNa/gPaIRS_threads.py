from .PaIRS_pypacks import*
import platform

if __package__ or "." in __name__:
  import PaIRS_UniNa.PaIRS_PIV as PaIRS_lib
else:
  import sys
  import platform
  if (platform.system() == "Darwin"):
    sys.path.append('../lib/mac')
  else:
    #sys.path.append('PaIRS_PIV')
    sys.path.append('../lib')
  import PaIRS_PIV as PaIRS_lib

#import PaIRS_UniNa.PaIRS_PIV as PaIRS_lib
from .Import_Tab import INPpar as INPpar
from .Export_Tab import OUTpar as OUTpar
from .Process_Tab import PROpar as PROpar

FlagTypeOfStop=1
FlagStopWorkers=[0]


class PIVpar: 
    def __init__(self):
        self.INP=INPpar()
        self.OUT=OUTpar()
        self.PRO=PROpar('simple','fast')
        self.list_Image_Files=[]
        self.list_eim=[]
        self.list_pim=[]
        self.i=-1
        self.nimg=-1
        self.NumThreads=-1
        self.NumThreads_PIV=1

        self.cont=0
        self.icont=0
        self.x=np.array([]) 
        self.y=np.array([])
        self.u=np.array([])
        self.v=np.array([])
        self.sn=np.array([])
        self.Info=np.array([])
        
    def setPIV(self):
        self.PIV=UIpar2PIV(self) 
        
    def duplicate(self):
        newist=PIVpar()
        for f,v in self.__dict__.items():
            if type(v) in (INPpar,OUTpar,PROpar):
                setattr(newist,f,v.duplicate())
            else:
                setattr(newist,f,copy.deepcopy(v))
        return newist

class PIV_Manager_Signals(QObject):
    error = Signal(tuple)
    progress = Signal(int,int,int,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,str)
    result   = Signal(int,int,int,int,np.ndarray,np.ndarray,np.ndarray,np.ndarray,str)
    finished = Signal(object)
    kill = Signal()
    goOn = Signal(int)

class PIV_Manager(QRunnable):
    def __init__(self,par=PIVpar,indWorker=int,indProc=int):
        super(PIV_Manager, self).__init__(par)
        self.par = par.duplicate()
        self.indWorker=indWorker
        self.indProc=indProc
        
        self.signals = PIV_Manager_Signals()
        self.isKilled = False
        self.isCommunicating=True
        self.indWorker = indWorker
        self.indProc = indProc        

        #parameters which are not updated can be put in self instead of self.par
        self.nimg_tot=len(self.par.list_Image_Files)
        self.currpath=myStandardPath(self.par.OUT.path+self.par.OUT.subfold)
        self.root=self.par.OUT.root
        self.ndig=self.par.INP.pinfo.ndig
        self.outType=self.par.OUT.outType
        if self.outType==0:
            self.ext='.mat'
        elif self.outType==1:
            self.ext='.plt'
        else:
            self.ext='.mat'
        #

    @Slot()
    def run(self):
        myprint(f'\nBeginning of PIV Manager ({self.indWorker})')
        while not self.isKilled:
            time.sleep(SleepTime_Workers)
        if self.par.icont<self.par.nimg:
            myprint(f'\nFinished signal')
            self.isKilled=False
            self.signals.finished.emit(self.par)
            while not self.isKilled:
                time.sleep(SleepTime_Workers)
        myprint(f'\nEnd of PIV Manager ({self.indWorker})')

    @Slot()
    def die(self):
        self.killWorkers()
        self.isKilled=True

    @Slot()
    def killWorkers(self):
        global FlagStopWorkers
        FlagStopWorkers[0]=1
        self.signals.kill.emit()
    
    @Slot(int)
    def updateIndProc(self,indProc):
        self.indProc=indProc

    @Slot(int,int,int,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray,str)
    def save_vector_fields(self,i,ithread,pim,x,y,u,v,sn,Info,stampa):
        self.par.list_pim[i]=pim
        self.par.icont+=1  #number of Trues in list_pim
        self.signals.result.emit(i,self.par.icont,self.indWorker,pim,x,y,u,v,stampa)

        if pim==1:    
            self.par.cont+=1  #number of images correctly processed
            Var=[x,y,u,v,sn,Info]
            self.saveResults(i,Var)
            if not np.size(self.par.u):
                self.par.x=x
                self.par.y=y
                self.par.u=u
                self.par.v=v
                self.par.sn=sn
                self.par.Info=Info
            else:
                self.par.u+=u
                self.par.v+=v
                self.par.sn+=sn
                self.par.Info+=Info

        if self.par.icont==self.par.nimg:
            u_mean=self.par.u/self.par.cont
            v_mean=self.par.v/self.par.cont
            sn_mean=self.par.sn/self.par.cont
            Info_mean=self.par.Info/self.par.cont
            Var=[self.par.x,self.par.y,u_mean,v_mean,sn_mean,Info_mean]
            self.saveResults(-1,Var)
            self.signals.finished.emit(self.par)
            self.die()


    def saveResults(self,i,Var):
        if i<0:
            nameFileOut=os.path.join(f"{self.currpath}{self.root}{self.ext}")
        else:
            nameFileOut=os.path.join(f"{self.currpath}{self.root}_{i:0{self.ndig:d}d}{self.ext}")
        #myprint(f'\nsaving field #{i}: {nameFileOut}')
        nameVar=['X', 'Y', 'U', 'V', 'Fc', 'info']
        if self.ext=='.plt':
            writePlt(nameFileOut, Var,'b16',nameVar,nameFileOut)
        elif  self.ext=='.mat':
            dict_out={}
            for j in range(len(nameVar)):
                dict_out[nameVar[j]]=Var[j]
            scipy.io.savemat(nameFileOut,dict_out)

class PIV_Worker(PIV_Manager):
    @Slot()
    def run(self):
        try:
            while self.indWorker!=self.indProc and not self.isKilled:
                time.sleep(SleepTime_Workers)
            myprint(f'\nBeginning of PIV Worker ({self.indWorker})')
            self.runPIVCycle()
        except:
            myprint('\n!!! error from PIV_Worker')
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            if self.par.icont<self.par.nimg:
                myprint(f'\nFinished signal')
                self.isKilled=False
                self.signals.finished.emit(self.par)
                while not self.isKilled:
                    time.sleep(SleepTime_Workers)
            #if self.isKilled: self.signals.finished.emit(self.par)
            myprint(f'\nEnd of PIV Worker ({self.indWorker}.{self.par.i})')

    def runPIVCycle(self):
        PIV=UIpar2PIV(self.par)
        Image2PIV_Float=Image2Float( np.float64 if PIV.SizeOfReal()==8 else np.float32)
        PIV.Inp.FlagNumThreads=self.par.NumThreads_PIV
        PIV.Inp.FlagLog=0
        #myprint(f"{self.par.PRO.Vect},   type={type(self.par.PRO.Vect[0])}")
        vect=[]
        for v in self.par.PRO.Vect:
            vect.append(v.astype(np.intc))
        PIV.SetVect(vect)

        if self.par.INP.flag_min:
            Imin=[]
            currpath=myStandardPath(self.par.OUT.path+self.par.OUT.subfold)
            root=myStandardRoot(self.par.OUT.root)
            ext=self.par.INP.pinfo.ext
            for j,f in enumerate('ab'):
                nameout=f"{currpath}{root}_{f}_min{ext}"
                if os.path.exists(nameout):
                    Imin.append(Image2PIV_Float(Image.open(nameout)))
                    #myprint(f'\nMinimum image for frame {f} loaded.')
            Imin=transfIm(self.par.OUT,Imin[0],Imin[1])

        if FlagTypeOfStop==0:
            FunOut=PaIRS_lib.PythonOutFromPIV()
            fun=PaIRS_lib.GetPyFunction(FunOut)
        else:
            global FlagStopWorkers
            FlagStopWorkers[0]=0
            FunOut=WrapperOutFromPIV_Worker()
            fun=PaIRS_lib.GetPyFunction(FunOut)

        i=self.par.i
        di=self.par.NumThreads
        while i<self.par.nimg:
            if not self.par.list_pim[i]:
                j=i*2
                if self.par.list_eim[j] and self.par.list_eim[j+1]:  
                    if self.isKilled: 
                        i-=di
                        return
                    name_a=self.par.INP.path+self.par.list_Image_Files[j]
                    I=Image.open(name_a)
                    Ia=Image2PIV_Float(I)
                    if self.par.INP.flag_min:
                        Ia=Ia-Imin[0]
                    if self.isKilled: 
                        i-=di
                        return
                    I=Image.open(self.par.INP.path+self.par.list_Image_Files[j+1])
                    Ib=Image2PIV_Float(I)
                    if self.par.INP.flag_min:
                        Ib=Ib-Imin[1]
                    if self.isKilled: 
                        i-=di
                        return
                    Iproc=transfIm(self.par.OUT,Ia,Ib)
                    PIV.SetImg(Iproc)
                    #myprint(os.getpid())
                    try:
                        err=PIV.PIV_Run(fun)
                        if err==-1000: #interrotto 
                            x=y=u=v=sn=Info=np.array([])
                            self.par.list_pim[i]=0 #useless
                            myprint(f'\nWorker #{self.par.i}: I was stopped in PIV_Run!')
                            i-=di 
                            return
                        else:
                            x,y,u,v=transfVect(self.par.OUT,PIV)
                            sn=np.asarray(PIV.sn).copy()
                            Info=np.asarray(PIV.Info).copy()
                            self.par.list_pim[i]=1
                        stampa=printPIVLog(PIV)
                        stampa=name_a+'\n'+stampa
                    except SystemError as inst:
                        myprint('\n*********** ERROR from the LIBRARY PaIRS_PIV! ***********')
                        myprint(inst.__cause__)
                        x=y=u=v=sn=Info=np.array([])
                        self.par.list_pim[i]=-1 #useless       
                        stampa=name_a+"\nError while processing the above image pair:\n" +str(inst.__cause__)        
                else:
                    x=y=u=v=sn=Info=np.array([])
                    self.par.list_pim[i]=-2
                    stampa=name_a+"\nError while processing the above image pair:\n"+\
                        "One of the images does not exist!"
                self.signals.progress.emit(i,self.par.i,self.par.list_pim[i],x,y,u,v,sn,Info,stampa)
            i+=di

        myprint(f'\n***** End of PIV_Worker #{self.par.i} cycle ({self.par.i}:{i-di}:{di})! *****')
        while not self.isKilled:# and FlagStopWorkers:
            time.sleep(SleepTime_Workers)

    @Slot()
    def die(self):
        global FlagStopWorkers
        FlagStopWorkers[0]=1
        self.isKilled=True

def printPIVLog(PIV):
    stampa="It    IW      #IW        #Vect/#Tot      %       CF       CF(avg)   DC%\n"#  NR% Cap%\n"
    for j in range(len(PIV.PD.It)):
        riga="%3d %3dx%-3d %4dx%-4d %7d/%-7d %5.1f  %8.7f  %8.7f  %4.1f\n" %\
            (PIV.PD.It[j], PIV.PD.WCella[j], PIV.PD.HCella[j], PIV.PD.W[j], PIV.PD.H[j], PIV.PD.NVect[j],\
            PIV.PD.W[j]*PIV.PD.H[j], 100.0*PIV.PD.NVect[j]/(PIV.PD.W[j]*PIV.PD.H[j]), PIV.PD.Fc[j],\
                PIV.PD.FcMedia[j], 100.0*PIV.PD.ContErorreDc[j]/(PIV.PD.W[j]*PIV.PD.H[j]))#,\
                    #100.0*PIV.PD.ContRemNoise[j]/(PIV.Inp.ImgW*PIV.Inp.ImgH),\
                    #100.0*PIV.PD.ContCap[j]/(PIV.Inp.ImgW*PIV.Inp.ImgH))
        stampa=stampa+riga
    return stampa

def transfIm(OUT,*args):
    Imout=[]
    for i in range(len(args)):
        Ima=args[i][OUT.y:OUT.y+OUT.h,OUT.x:OUT.x+OUT.w].copy()
        for op in OUT.bimop:
            if op==1:  #rot 90 counter
                Ima=np.rot90(Ima,1)
            elif op==-1: #rot 90 clock
                Ima=np.rot90(Ima,-1)
            elif op==3: #flip
                Ima=np.flipud(Ima)
            elif op==2:
                Ima=np.fliplr(Ima)
        Imout.append(np.ascontiguousarray(Ima))
    return Imout


def transfVect(OUT,PIV):
    x0=np.asarray(PIV.x).copy()
    y0=np.asarray(PIV.y).copy()
    u0=np.asarray(PIV.u).copy()
    v0=np.asarray(PIV.v).copy()
    for op in OUT.aimop:
        if op==1:  #rot 90 counter
            u=+v0
            v=-u0
            x=+y0
            y=-x0
        elif op==-1: #rot 90 clock
            u=-v0
            v=+u0
            x=-y0
            y=+x0
        elif op==3: #flip
            u=-u0
            x=-x0
        elif op==2:
            v=-v0
            y=-y0
        if op:
            u0=u.copy()
            v0=v.copy()
            x0=x.copy()
            y0=y.copy()
    return x0,y0,u0,v0


class WrapperOutFromPIV_Worker(PaIRS_lib.PyFunOutPIV) :
    ''' Wrapper class for FunOut 
    FunOut is called periodically from the PaIRS_PIV lib and if FunOut returns a value different from 
    zero the processing is stopped
    '''
    def __init__(self):
        PaIRS_lib.PyFunOutPIV.__init__(self)
    def FunOut(self,a,b,o):
        return FlagStopWorkers[0]
        
def Image2Float(a): 
    return lambda I: np.ascontiguousarray(I,dtype= a)

def UIpar2PIV(par):
    PIV=PaIRS_lib.PIV()
    
    PIV.DefaultValues()
    OUT=par.OUT
    PRO=par.PRO

    PIV.Inp.RisX=OUT.xres*float(10.0)
    PIV.Inp.RisY=OUT.xres*OUT.pixAR*float(10.0)
    PIV.Inp.dt=OUT.dt
    PIV.Inp.ImgH=OUT.h
    PIV.Inp.ImgW=OUT.W

    PIV.Inp.SogliaNoise=PRO.SogliaNoise
    PIV.Inp.SogliaStd=PRO.SogliaStd
    PIV.Inp.SogliaMed=PRO.SogliaMed

    PIV.Inp.SogliaMedia=PRO.SogliaMedia
    PIV.Inp.SogliaNumVet=PRO.SogliaNumVet

    if PRO.FlagNogTest: PIV.Inp.FlagValid=3
    else:
        if PRO.FlagMedTest:
            i=PRO.KernMed
            if PRO.TypeMed==0:
                if not PRO.FlagSecMax: PIV.Inp.FlagValid=1+6*(i-1)
                else: PIV.Inp.FlagValid=2+6*(i-1)
            elif PRO.TypeMed==1:
                if not PRO.FlagSecMax: PIV.Inp.FlagValid=4+6*(i-1)
                else: PIV.Inp.FlagValid=5+6*(i-1)
        else:
            if PRO.FlagSNTest: 
                PIV.Inp.FlagValid=0
                PIV.Inp.SogliaSN=PRO.SogliaSN
            elif  PRO.FlagCPTest:
                PIV.Inp.FlagValid=0
                PIV.Inp.SogliaSN=PRO.SogliaCP

    PIV.Inp.IntIniz=PRO.IntIniz
    PIV.Inp.IntFin=PRO.IntFin
    PIV.Inp.FlagInt=PRO.FlagInt
    PIV.Inp.IntVel=PRO.IntVel 
    PIV.Inp.CorrezioneVel=PRO.FlagCorrezioneVel
    PIV.Inp.IntCorr=PRO.IntCorr 
    PIV.Inp.FlagWindowing=PRO.FlagWindowing
    PIV.Inp.SemiDimCalcVel=PRO.SemiDimCalcVel

    PIV.Inp.MaxC=PRO.MaxC
    PIV.Inp.MinC=PRO.MinC
    PIV.Inp.LarMin=PRO.LarMin
    PIV.Inp.LarMax=PRO.LarMax

    PIV.Inp.FlagCalcVel=PRO.FlagCalcVel
    PIV.Inp.FlagSommaProd=PRO.FlagSommaProd
    PIV.Inp.FlagDirectCorr=PRO.FlagDirectCorr
    PIV.Inp.FlagBordo=PRO.FlagBordo

    PIV.Inp.NIterazioni=PRO.NIterazioni

    return PIV


