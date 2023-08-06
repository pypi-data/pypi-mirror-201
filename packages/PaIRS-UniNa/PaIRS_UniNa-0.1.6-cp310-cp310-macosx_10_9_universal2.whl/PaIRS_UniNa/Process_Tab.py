from .ui_Process_Tab import*
from .TabTools import*
from .Custom_Top import Custom_Top

Flag_type_of_DCs=False
Flag_Hart_corr=False
Flag_Nogueira=False

mode_items= ['simple', #0
             'advanced', #1
             'expert'] #2

top_items=[ 'custom',  #0
            'preview', #1
            'fast',    #2
            'standard',#3
            'advanced',#4
            'high resolution', #5
            'adaptative resolution'] #6

mode_init=mode_items[0]
top_init=top_items[3]

ImInt_items=( #************ do not change the order of items here!
            'none',                             # none
            'moving window',                    # moving window
            'linear revitalized',               # linear revitalized
            'bilinear/biquadratic/bicubic',     # bilinear/biquadratic/bicubic
            'simplex',                          # simplex
            'shift theorem',                    # shift theorem
            'sinc (Whittaker-Shannon)',         # sinc (Whittaker-Shannon)
            'B-spline'                          # B-spline
            )
ImInt_order=[i for i in range(8)] #************ change here, please!

VelInt_items=( #************ do not change the order of items here!
            'bilinear',                         # bilinear
            'linear revitalized',               # linear revitalized
            'simplex',                          # simplex
            'shift theorem',                    # shift theorem
            'shift theorem (extrapolation)',    # shift theorem (extrapolation)
            'B-spline'                          # B-spline
            )
VelInt_order=[i for i in range(7)] #************ change here, please!


Wind_items=( #************ do not change the order of items here!
            'top-hat',                          # top-hat
            'Nogueira',                         # Nogueira
            'Blackman',                        # Blackman
            'Blackman-Harris',                 # Blackman-Harris
            'triangular',                       # Triangular
            'Hann',                             # Hann
            'Gaussian',                         # Gaussian
            )
#Wind_order=[i for i in range(8)] #************ change here, please!
Wind_order=[0,2,6,3,5,1,4]

def cont_fields(diz):
    cont=0
    for f,v in diz:
        if not 'fields' in f and f[0]!='_':
            cont+=1
    return cont
    
class PROpar(TABpar):
    mode=mode_init

    def __init__(self,*args):
        top=top_init
        if len(args):
            top=args[0]
        #attributes in fields
        self.setup(top)
        super().__init__()
        self.name='PROpar'
        self.surname='PROCESS_Tab'
        self.unchecked_fields+=['prev_top','top','mode',\
            'FlagFinIt_reset','FlagInterp_reset','FlagValidation_reset','FlagWindowing_reset','FlagCustom',\
            'VectFlag','flag_rect_wind']

    def setup(self,top):
        cont=[0]
        name_fields=['']
        #************* DEFAULT VALUES
        #******************************* base_fields
        self.FlagCustom=False
        self.FlagFinIt_reset=False
        self.FlagInterp_reset=False
        self.FlagValidation_reset=False
        self.FlagWindowing_reset=False

        if not self.mode in mode_items:
            self.mode=mode_items[0]
        self.top=top
        self.prev_top=top_items.index(top)

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('base')

        #******************************* IW_fields
        WSize_init=[128, 64, 32]
        WSpac_init=[ 64, 16, 8]
        self.Nit=len(WSize_init)
        Vect=[np.array(WSize_init,np.intc), np.array(WSpac_init,np.intc),\
            np.array(WSize_init,np.intc), np.array(WSpac_init,np.intc)]
        self.Vect=Vect
        self.VectFlag=[True]*4
        self.flag_rect_wind=False
        self.FlagBordo=1

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('IW')

        #******************************* Int_fields
        self.IntIniz=1
        self.IntFin=1
        self.FlagInt=0
        self.IntCorr=0
        self.IntVel=1

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('Int')

        #******************************* FinalIt_fields
        self.FlagDirectCorr=1
        self.NIterazioni=0

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('FinalIt')

        #******************************* Validation_fields
        self.FlagMedTest=1
        self.TypeMed=1
        self.KernMed=1
        self.SogliaMed=2.0
        self.ErroreMed=0.5

        self.FlagSNTest=0
        self.SogliaSN=1.5

        self.FlagCPTest=0
        self.SogliaCP=0.2

        self.FlagNogTest=0
        self.SogliaMedia=0.25
        self.SogliaNumVet=0.10

        self.SogliaNoise=2.00
        self.SogliaStd=3.00
        self.FlagCorrezioneVel=1
        self.FlagSecMax=1
        self.FlagCorrHart=0

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('Validation')

        #******************************* Windowing_fields
        self.FlagCalcVel=0
        self.FlagWindowing=0
        self.SemiDimCalcVel=0

        self.FlagAdaptative=0
        self.NItAdaptative=2
        self.MinC=0.4
        self.MaxC=0.75
        self.LarMin=1
        self.LarMax=16
        self.FlagSommaProd=0
        
        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('Wind')

        
        if self.top==top_items[1] : #preview/custom
            self.IntIniz=3
            self.IntFin=3
            self.IntVel=1
            self.NIterazioni=0
        elif self.top==top_items[2]: #fast
            self.IntIniz=1
            self.IntFin=1
            self.IntVel=1
            self.NIterazioni=1
        elif self.top==top_items[0] or self.top==top_items[3]: #standard
            self.IntIniz=53
            self.IntFin=53
            self.IntVel=52
            self.NIterazioni=2
        elif self.top==top_items[4]: #advanced
            self.IntIniz=57
            self.IntFin=57
            self.IntVel=53
            self.NIterazioni=2

            self.FlagCalcVel=2
            self.FlagWindowing=2
        elif self.top==top_items[5]: #high resolution
            self.IntIniz=57
            self.IntFin=57
            self.IntVel=53
            self.NIterazioni=10

            self.FlagCalcVel=2
            self.FlagWindowing=2
            self.SemiDimCalcVel=3
        elif self.top==top_items[6]: #adaptative
            self.IntIniz=57
            self.IntFin=57
            self.IntVel=53
            self.NIterazioni=20

            self.FlagCalcVel=2
            self.FlagWindowing=2
            self.FlagAdaptative=1
        
        for j in range(1,len(cont)):
            setattr(self,name_fields[j]+"_fields",[])
            d=getattr(self,name_fields[j]+"_fields")
            k=-1
            for f,_ in self.__dict__.items():
                k+=1
                if k in range(cont[j-1],cont[j]):
                    d.append(f)

    def change_top(self,top_new):
        newist=PROpar(top_new)
        for f in self.fields:
            if f not in self.IW_fields:
                setattr(self,f,getattr(newist,f))       

class Process_Tab(gPaIRS_Tab):
    class Process_Tab_Signals(gPaIRS_Tab.Tab_Signals):
        pass

    def __init__(self,*args):
        parent=None
        flagInit=True
        if len(args): parent=args[0]
        if len(args)>1: flagInit=args[1]
        super().__init__(parent,Ui_ProcessTab,PROpar)
        self.signals=self.Process_Tab_Signals(self)

        #------------------------------------- Graphical interface: widgets
        self.ui: Ui_ProcessTab
        ui=self.ui

        self.Vect_widgets=[ui.line_edit_size,\
            ui.line_edit_spacing,\
                ui.line_edit_size_2,\
                    ui.line_edit_spacing_2]
        self.Vect_Lab_widgets=[ui.check_edit_size,\
            ui.check_edit_spacing,\
                ui.check_edit_size_2,\
                    ui.check_edit_spacing_2]
        ui.line_edit_size.addlab=ui.check_edit_size
        ui.line_edit_size.addwid=[w for w in self.Vect_widgets]
        ui.line_edit_size.addwid.append(ui.spin_final_iter)
        ui.line_edit_spacing.addlab=ui.check_edit_spacing
        ui.line_edit_spacing.addwid=ui.line_edit_size.addwid
        ui.line_edit_size_2.addlab=ui.check_edit_size_2
        ui.line_edit_size_2.addwid=ui.line_edit_size.addwid
        ui.line_edit_spacing_2.addlab=ui.check_edit_spacing_2
        ui.line_edit_spacing_2.addwid=ui.line_edit_size.addwid

        #necessary to change the name and the order of the items
        ui.combo_mode.clear()
        for item in mode_items:
            ui.combo_mode.addItem(item)
        ui.combo_top.clear()
        for item in top_items:
            ui.combo_top.addItem(item)
        ui.combo_ImInt.clear()
        ui.combo_ImInt_2.clear()
        for i in range(len(ImInt_items)):
            ui.combo_ImInt.addItem(ImInt_items[ImInt_order[i]])
            ui.combo_ImInt_2.addItem(ImInt_items[ImInt_order[i]])        
        ui.combo_int_vel.clear()
        for i in range(len(VelInt_items)):
            ui.combo_int_vel.addItem(VelInt_items[VelInt_order[i]])
        ui.combo_Wind_Vel_type.clear()
        ui.combo_Wind_Corr_type.clear()
        for i in range(len(Wind_items)):
            ui.combo_Wind_Vel_type.addItem(Wind_items[Wind_order[i]])        
            ui.combo_Wind_Corr_type.addItem(Wind_items[Wind_order[i]])

        self.setupWid()  #---------------- IMPORTANT
        """
        ui.CollapBoxes=self.findChildren(CollapsibleBox)
        height_min=2^64
        for cb in ui.CollapBoxes:
            cb.setup()
            cb.initFlag=True
            if cb.heightOpened<height_min:
                height_min=cb.heightOpened

        for cb in ui.CollapBoxes:
            indx=ui.scrollAreaWidgetContents_PT.layout().indexOf(cb)
            cb.setup(indx,cb.heightOpened//height_min+1)
        """

        #------------------------------------- Graphical interface: miscellanea
        self.icon_plus = QIcon()
        self.icon_plus.addFile(u""+ icons_path +"plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_minus = QIcon()
        self.icon_minus.addFile(u""+ icons_path +"minus.png", QSize(), QIcon.Normal, QIcon.Off)

        self.Lab_greenv=QPixmap(u""+ icons_path +"greenv.png")
        self.Lab_redx=QPixmap(u""+ icons_path +"redx.png")
        self.Lab_warning=QPixmap(u""+ icons_path +"warning.png")

        self.ui.button_more_size.setIconSize(self.ui.button_more_size.size()-QSize(6,6))
        self.ui.button_more_iter.setIconSize(self.ui.button_more_iter.size()-QSize(6,6))

        self.custom_list_file=pro_path+custom_list_file
        self.PROpar_customs=[]
        self.custom_list=setCustomList(lambda var,name: self.PROpar_customs.append(var))
        self.updateCustomList(False)

        #------------------------------------- Declaration of parameters 
        self.PROpar_base=PROpar()
        self.PROpar:PROpar=self.TABpar
        self.PROpar_old:PROpar=self.TABpar_old
        self.defineSetTABpar(self.setPROpar)

        self.PROpar_custom=PROpar(self.PROpar.top)
        self.PROpar_custom.top='custom'

        #------------------------------------- Callbacks 
        self.setupCallbacks()

        #------------------------------------- Initializing    
        if flagInit:     
            self.initialize()

        #------------------------------------- obsolescences    
        if not Flag_type_of_DCs: self.ui.w_type_of_DCs.hide()
        if not Flag_Hart_corr: self.ui.check_Hart.hide()
        if not Flag_Nogueira: self.ui.w_Nogueira.hide()

    def initialize(self):
        pri.Info.yellow(f'{"*"*20}   PROCESS initialization   {"*"*20}')
        self.setTABpar(True)
        
    def setupCallbacks(self):
        #Callbacks
        self.defineIWCallbacks()    
        self.combo_custom_top_callback=self.combo_top_callback   
        self.defineInterpCallbacks() 
        self.defineWindowingCallbacks()
        self.defineCollapBoxCallbacks()

        spin_names=['final_iter','final_it','MedTest_ker','MedTest_alfa','MedTest_eps','SNTest_thres',\
                    'CPTest_thres','Nog_tol','Nog_numvec','MinVal','MinStD','Wind_halfwidth',\
                    'adaptative_iter','min_Corr','max_Corr','max_Lar','min_Lar',\
                    'order','order_2','VelInt_order','par_Gauss','par_Gauss_2']
        spin_tips=['Number of final iterations','Number of final iterations for different image interpolation','Semi-kernel for median test','Alpha threshold for median test','Epsilon threshold for median test','Threshold for S/N test',\
                    'Threshold for correlation peak test','Tolerance for Nogueira test','Number of vectors for Nogueira test','Minimum allowed value for validation','Minimum allowed st.d. value for validation','Weighting window half-width',\
                    'Number of iterations for adaptative process','Minimum correlation value for adapatative process','Maximum correlation value for adapatative process','Maximum half-width for adapatative process','Minimum half-width for adapatative process',\
                    'Kernel width for image interpolation','Kernel width for image interpolation (final it.)','Kernel width for velocity interpolation','Alpha threshold for Gaussian window','Half-width for Gaussian window']
        self.setSpinCallbacks(spin_names,spin_tips)
        self.ui.spin_final_it.addfuncout['check_more_iter']=self.check_more_iter
        self.ui.spin_final_it.addfuncreturn['check_more_iter']=self.check_more_iter

        signals=[["clicked"],
                 ["toggled"],
                 ["editingFinished"], #"returnPressed"  #***** inserire?
                 ["activated"],       #"currentIndexChanged"   #***** rimpiazzare?
                 ["toggled"],
                 ["clicked"]]
        fields=["button",
                "check",
                "line_edit",
                "combo",
                "radio",
                "push_CollapBox"]
        names=[ ['more_size','more_iter','edit_custom'], #button
                ['flag_boundary','DC','second_peak','Hart'], #check
                ['size','spacing','size_2','spacing_2'], #edit
                ['mode','top','custom_top','correlation','MedTest_type','Correction_type','type_of_DCs',\
                 'ImInt','par_pol','par_imshift','ImInt_2','par_pol_2','par_imshift_2','int_vel',\
                 'Wind_Vel_type','par_tophat','par_Nog','par_Bla','par_Har',\
                 'Wind_Corr_type','par_tophat_2','par_Nog_2','par_Bla_2','par_Har_2'], #combo
                ['MedTest','SNTest','CPTest','Nogueira','Adaptative'], #radio
                  ['FinIt','Interp','Validation','Windowing','top']] #push
        tips=[ ['Rectangular IW','Image interpolation (final it.)','Custom type of process'], #button
                ['First vector at IW spacing','Direct correlation','Second correlation peak correction','Hart''s correction'], #check
                ['IW size','IW spacing','IW size','IW spacing'], #edit
                ['Process mode','Type of process','Custom type of process','Correlation map interpolation','Median test type','Correction type','Type of DCs',\
                 'Image interpolation','Polynomial interpolation','Moving window','Image interpolation (final it.)','Polynomial interpolation (final it.)','Moving window (final it.)','Velocity field interpolation',\
                 'Velocity weighting window','Top-hat window type (vel.)','Nogueira window type (vel.)','Blackman window type (vel.)','Blackman-Harris window type (vel.)',\
                 'Correlation map weighting window','Top-hat window type (corr.)','Nogueira window type (corr.)','Blackman window type (corr.)','Blackman-Harris window type (corr.)'], #combo
                ['Median test','S/N test','Correlation peak test','Nogueira test','Adaptative process'], #radio
                  ['Final iteration  box','Interpolation box','Validation box','Windowing box','Type of process box']] #push
        
        for f,N,S,T in zip(fields,names,signals,tips):
            for n,t in zip(N,T):
                wid=getattr(self.ui,f+"_"+n)
                fcallback=getattr(self,f+"_"+n+"_callback")
                fcallbackWrapped=self.addParWrapper(fcallback,t)
                for s in S:
                    sig=getattr(wid,s)
                sig.connect(fcallbackWrapped)

        #graphical callbacks
        names=['size','spacing','size_2','spacing_2']
        f='line_edit'
        for n in names:
            wid=getattr(self.ui,f+"_"+n)
            fcallback=getattr(self,f+"_"+n+"_changing")
            wid.textChanged.connect(fcallback)
        
        #other functions
        self.ui.button_save_custom.clicked.connect(self.button_save_custom_callback)

    def defineIWCallbacks(self):
        def setIWCallback(i):
            j=i
            widname=f+"_"+n
            a1=getattr(self.ui,'line_edit'+'_'+n)
            a2=getattr(self.ui,'check_edit'+'_'+n)
            foutmeth_name=widname+'_changing'
            setattr(self,foutmeth_name,lambda: self.edit_Wind_vectors(a1,a2))
            foutmeth_name=widname+'_callback'
            setattr(self,foutmeth_name,lambda: self.set_Wind_vectors(a1,a2,j))
        names=['size','spacing','size_2','spacing_2']
        f='line_edit'
        for i,n in enumerate(names):
            setIWCallback(i)
        return
    
    def defineInterpCallbacks(self):
        self.combo_ImInt_callback=lambda: self.combo_ImInt_action(self.ui.combo_ImInt,self.ui.w_ImInt_par)
        fmethod1=lambda: self.setImIntIndex(self.ui.combo_ImInt,self.ui.w_ImInt_par)
        names=['combo_par_pol','combo_par_imshift','spin_order']
        for n in names:
            setattr(self,n+'_callback',fmethod1)
        self.combo_ImInt_2_callback=lambda: self.combo_ImInt_action(self.ui.combo_ImInt_2,self.ui.w_ImInt_par_2)
        fmethod2=lambda: self.setImIntIndex(self.ui.combo_ImInt_2,self.ui.w_ImInt_par_2)
        names=['combo_par_pol_2','combo_par_imshift_2','spin_order_2']
        for n in names:
            setattr(self,n+'_callback',fmethod2)

        self.combo_int_vel_callback=lambda: self.combo_VelInt_action(self.ui.combo_int_vel,self.ui.w_VelInt_par)
        self.spin_VelInt_order_callback=lambda: self.setVelIntIndex(self.ui.combo_int_vel,self.ui.w_VelInt_par)
        return     

    def defineWindowingCallbacks(self):
        self.combo_Wind_Vel_type_callback=lambda: self.combo_Wind_callback(self.ui.combo_Wind_Vel_type,self.ui.w_Wind_par)
        fmethod1=lambda: self.setWindIndex(self.ui.combo_Wind_Vel_type,self.ui.w_Wind_par)
        names=['combo_par_tophat','combo_par_Nog','combo_par_Bla','combo_par_Har','spin_par_Gauss']
        for n in names:
            setattr(self,n+'_callback',fmethod1)

        self.combo_Wind_Corr_type_callback=lambda: self.combo_Wind_callback(self.ui.combo_Wind_Corr_type,self.ui.w_Wind_par_2)
        fmethod2=lambda: self.setWindIndex(self.ui.combo_Wind_Corr_type,self.ui.w_Wind_par_2)
        names=['combo_par_tophat_2','combo_par_Nog_2','combo_par_Bla_2','combo_par_Har_2','spin_par_Gauss_2']
        for n in names:
            setattr(self,n+'_callback',fmethod2)
        return

    def defineCollapBoxCallbacks(self):
        p=PROpar()
        self.push_CollapBox_FinIt_callback=lambda: self.reset_field(p.FinalIt_fields,self.ui.push_CollapBox_FinIt)
        self.push_CollapBox_Interp_callback=lambda: self.reset_field(p.Int_fields,self.ui.push_CollapBox_Interp)
        self.push_CollapBox_Validation_callback=lambda: self.reset_field(p.Validation_fields,self.ui.push_CollapBox_Validation)
        self.push_CollapBox_Windowing_callback=lambda: self.reset_field(p.Wind_fields,self.ui.push_CollapBox_Windowing)
        self.push_CollapBox_top_callback=self.combo_top_action
        return
   
 #*************************************************** PROpars and controls
    def reset_field(self,diz,push):
        top=self.ui.combo_top.itemText(self.PROpar.prev_top)
        PROpar_old=PROpar(top)
        self.PROpar.copyfromdiz(PROpar_old,diz)
        if self.PROpar.top=='custom':
            self.setPROpar_custom()

    def setPROpar_custom(self):
        fields=[f for f in self.PROpar.fields if not f in self.PROpar.IW_fields+['ind','indItem','indTree']]
        i=self.ui.combo_custom_top.currentIndex()
        if len(self.PROpar_customs) and i>-1:
            self.PROpar.copyfromdiz(self.PROpar_customs[i],fields)
        else:
            self.PROpar.copyfromdiz(self.PROpar_custom,fields)
    
    def check_reset(self):
        PROpar_old=PROpar(self.PROpar.top)
        if PROpar_old.top=='custom':
            i=self.ui.combo_custom_top.currentIndex()
            if i!=-1:
                PROpar_old.copyfrom(self.PROpar_customs[i])
        exc=self.PROpar.unchecked_fields+['indTree','indItem','ind']
        self.PROpar.FlagFinIt_reset=not self.PROpar.isEqualTo(PROpar_old,exc,self.PROpar.FinalIt_fields)
        self.PROpar.FlagInterp_reset=not self.PROpar.isEqualTo(PROpar_old,exc,self.PROpar.Int_fields)
        self.PROpar.FlagValidation_reset=not self.PROpar.isEqualTo(PROpar_old,exc,self.PROpar.Validation_fields)
        self.PROpar.FlagWindowing_reset=not self.PROpar.isEqualTo(PROpar_old,exc,self.PROpar.Wind_fields)
        self.PROpar.printDifferences(PROpar_old,exc)
        self.PROpar.FlagCustom=self.PROpar.FlagFinIt_reset|self.PROpar.FlagInterp_reset|\
            self.PROpar.FlagValidation_reset|self.PROpar.FlagWindowing_reset
        self.setPushCollapBoxes()

    def button_save_custom_callback(self):
        name=self.save_as_custom()
        if name!='':
            if name in self.custom_list:
                k=self.custom_list.index(name)
                self.custom_list.pop(k)
            self.custom_list.insert(0,name)
            self.PROpar_customs.insert(0,self.PROpar.duplicate())
            self.updateCustomList(True)

        self.FlagAddFunc=False
        self.PROpar.top='custom'
        self.PROpar.FlagCustom=False
        self.setPROpar_ToP()
        self.check_reset()
        self.PROpar_custom.copyfrom(self.PROpar)
        self.FlagAddFunc=True

    def save_as_custom(self):
        title="Save custom type of process"
        label="Enter the name of the custom type of process:"
        ok,text=self.inputDialog(title,label,completer_list=self.custom_list)

        if ok and text!='':
            filename=pro_path+text+outExt.pro
            if os.path.exists(filename):
                Message=f'Process "{text}" already exists.\nDo you want to overwrite it?'
                flagOverwrite=self.questionDialog(Message)
                if not flagOverwrite: return
                FlagValidRoot=True
            else:
                dummyfilename=pro_path+text+outExt.dum
                try:
                    open(dummyfilename,'w')
                except:
                    FlagValidRoot=False
                else:
                    FlagValidRoot=True
                finally:
                    if os.path.exists(dummyfilename):
                        os.remove(dummyfilename)
            if not FlagValidRoot: 
                warningDialog(self,'Invalid root name! Please, retry.')
                return
            
            try:
                with open(filename,'wb') as file:

                    self.PROpar.top='custom'
                    self.PROpar.FlagCustom=False
                    self.PROpar.name=text

                    pickle.dump(self.PROpar,file)
                    pri.Info.blue(f'Saving custom process file {filename}')
            except Exception as inst:
                pri.Error.red(f'Error while saving custom process file {filename}:\n{traceback.print_exc}\n\n{inst}')
                text=''
        return text

    def updateCustomList(self,FlagRewrite):
        if FlagRewrite:
            rewriteCustomList(self.custom_list)
        self.ui.combo_custom_top.clear()
        self.ui.combo_custom_top.addItems(self.custom_list) 

    def button_edit_custom_callback(self):
        self.edit_dlg = Custom_Top(self.custom_list)
        self.edit_dlg.close=lambda: self.edit_dlg.done(0)
        self.edit_dlg.exec()
        #self.custom_list=self.edit_dlg.custom_list 
        self.edit_dlg.close()
        self.PROpar_customs=[]
        self.custom_list=setCustomList(lambda var,name: self.PROpar_customs.append(var))
        currentItem=self.ui.combo_custom_top.currentText()
        self.updateCustomList(False)
        if currentItem in self.custom_list:
            i=self.custom_list.index(currentItem)
        else:
            i=-1
        self.ui.combo_custom_top.setCurrentIndex(i)
        self.PROpar_custom.copyfrom(self.PROpar)
        return [0,None]

#*************************************************** From Parameters to UI
    def setPROpar(self):
        #pri.Time.blue(1,'setPROpar: Beginning')
        self.ui.combo_mode.setCurrentIndex(self.ui.combo_mode.findText(self.PROpar.mode))
        self.setMode()
        self.setPROpar_IW()
        self.setPROpar_FinIt()
        self.setPROpar_ToP()
        self.setPROpar_Int()
        self.setPROpar_Valid()
        self.setPROpar_Wind()
        self.check_reset()
        #pri.Time.blue(0,'setPROpar: end')
    
    def setPushCollapBoxes(self,*args):
        if len(args): 
            cb=args #tuple
        else: 
            cb=('FinIt','Interp','Validation','Windowing','ToP')
        for n in cb:
            if n!='ToP':
                flag=getattr(self.PROpar,'Flag'+n+'_reset')
                push=getattr(self.ui,'push_CollapBox_'+n)
                CollapBox=getattr(self.ui,'CollapBox_'+n)
                if flag:
                    push.show() 
                else:
                    push.hide()
                CollapBox.FlagPush=flag
        if self.PROpar.FlagCustom:
            self.ui.button_save_custom.show()
            self.ui.label_top.setText("Modified from ")
            self.ui.push_CollapBox_top.show() 
            self.ui.CollapBox_top.FlagPush=True
        else:
            self.ui.button_save_custom.hide()
            self.ui.label_top.setText("Current")
            self.ui.push_CollapBox_top.hide() 
            self.ui.CollapBox_top.FlagPush=False

    def setPROpar_IW(self):
        #Interrogation Windows
        self.ui.button_more_size.setChecked(self.PROpar.flag_rect_wind)
        self.button_more_size_check()
        self.setVect()
        self.ui.check_flag_boundary.setChecked(not self.PROpar.FlagBordo==0)
    
    def setPROpar_FinIt(self):
        #Final iterations
        self.ui.spin_final_iter.setValue(self.PROpar.NIterazioni)
        self.ui.check_DC.setChecked(self.PROpar.FlagDirectCorr)

    def setPROpar_ToP(self):
        #Type of process
        i=self.ui.combo_top.findText(self.PROpar.top)
        self.ui.combo_top.setCurrentIndex(i)
        flag=i==0
        if flag:
            self.ui.w_custom_top.show()
        else:
            self.ui.w_custom_top.hide()
        if flag:
            flagEn=bool(len(self.custom_list))
            if flagEn:
                self.ui.label_custom_top.setText('Custom types')
            else:
                self.ui.label_custom_top.setText('No custom types available')
            self.ui.combo_custom_top.setEnabled(flagEn)
            #self.ui.button_edit_custom.setEnabled(flagEn)
            if flagEn:
                FlagCustom,i=self.checkFlagCustom()
                if not FlagCustom:  
                    self.ui.combo_custom_top.setCurrentIndex(i)
                #self.check_reset()
                
    def checkFlagCustom(self):
        i=-1
        fields=['name']+self.PROpar.FinalIt_fields+self.PROpar.Int_fields+self.PROpar.Validation_fields+self.PROpar.Wind_fields
        for k,p in enumerate(self.PROpar_customs):
            if p.isEqualTo(self.PROpar,[],fields): i=k
        FlagCustom=i==-1
        return FlagCustom,i

    def setPROpar_Int(self):
        #Interpolation
        self.ImIntIndex2UiOptions(self.PROpar.IntIniz,self.ui.combo_ImInt,self.ui.w_ImInt_par)
        self.ImIntIndex2UiOptions(self.PROpar.IntFin,self.ui.combo_ImInt_2,self.ui.w_ImInt_par_2)
        self.ui.button_more_iter.setChecked(int(self.PROpar.FlagInt))
        self.button_more_iter_check()
        self.ui.combo_correlation.setCurrentIndex(self.PROpar.IntCorr)
        self.VelIntIndex2UiOptions(self.PROpar.IntVel,self.ui.combo_int_vel,self.ui.w_VelInt_par)

    def setPROpar_Valid(self):
        #Validation
        self.setValidationType()
        self.ui.spin_MinVal.setValue(self.PROpar.SogliaNoise)
        self.ui.spin_MinStD.setValue(self.PROpar.SogliaStd)
        self.ui.combo_Correction_type.setCurrentIndex(self.PROpar.FlagCorrezioneVel)
        self.ui.check_second_peak.setChecked(int(self.PROpar.FlagSecMax))
        self.ui.check_Hart.setChecked(int(self.PROpar.FlagCorrHart))

    def setPROpar_Wind(self):
        #Windowing
        self.VelWindIndex2UiOptions(self.PROpar.FlagCalcVel,self.ui.combo_Wind_Vel_type,self.ui.w_Wind_par)
        self.VelWindIndex2UiOptions(self.PROpar.FlagWindowing,self.ui.combo_Wind_Corr_type,self.ui.w_Wind_par_2)
        self.ui.spin_Wind_halfwidth.setValue(self.PROpar.SemiDimCalcVel)
        self.ui.radio_Adaptative.setChecked(not self.PROpar.FlagAdaptative==0)
        self.radio_Adaptative_callback()
        self.ui.spin_adaptative_iter.setValue(self.PROpar.NItAdaptative)
        self.ui.spin_min_Corr.setValue(self.PROpar.MinC)
        self.spin_min_Corr_callback()
        self.ui.spin_max_Corr.setValue(self.PROpar.MaxC)
        self.spin_max_Corr_callback()
        self.ui.spin_min_Lar.setValue(self.PROpar.LarMin)
        self.spin_min_Lar_callback()
        self.ui.spin_max_Lar.setValue(self.PROpar.LarMax)
        self.spin_max_Lar_callback()
        self.ui.combo_type_of_DCs.setCurrentIndex(self.PROpar.FlagSommaProd)

#*************************************************** TYPE OF PROCESS
    def combo_top_callback(self):
        self.PROpar.top=self.ui.combo_top.currentText()
        self.combo_top_action()
            
    def combo_top_action(self):
        self.PROpar.prev_top=self.ui.combo_top.currentIndex()
        if self.PROpar.top=='custom':
            self.setPROpar_custom()
        else:
            self.PROpar.change_top(self.PROpar.top)
        return
    
#*************************************************** MODE   
    def combo_mode_callback(self):
        index=self.ui.combo_mode.currentIndex()
        PROpar.mode=mode_items[index]
        self.setMode()
        #for PRO in self.PROpar_prev:
        #    PRO.mode=self.PROpar.mode
        return [-1,None]
    
    def setMode(self):
        index=mode_items.index(PROpar.mode)
        if index==0:
            self.ui.CollapBox_Interp.hide()
            self.ui.CollapBox_Validation.hide()
            self.ui.CollapBox_Windowing.hide()
        elif index==1:
            self.ui.CollapBox_Interp.show()
            self.ui.CollapBox_Validation.hide()
            self.ui.CollapBox_Windowing.hide()
        elif index==2:
            self.ui.CollapBox_Interp.show()
            self.ui.CollapBox_Validation.show()
            self.ui.CollapBox_Windowing.show()

#*************************************************** INTERROGATION WINDOWS
    def setVect(self):
        for i in range(len(self.Vect_widgets)):
            w=self.Vect_widgets[i]
            v=self.PROpar.Vect[i]
            l=self.Vect_Lab_widgets[i]
            text="".join([str(t)+", " for t in v[:-1]]) + str(v[-1])
            w.setText(text)
            if self.PROpar.VectFlag[i]:
                l.setPixmap(self.Lab_greenv)
                l.setToolTip('')
            else:
                l.setPixmap(self.Lab_redx)
        self.check_more_iter()
   
    def button_more_size_callback(self):
        self.PROpar.flag_rect_wind=not self.PROpar.flag_rect_wind
        if not self.PROpar.flag_rect_wind:
            self.PROpar.Vect[2]=self.PROpar.Vect[0].copy()
            self.PROpar.Vect[3]=self.PROpar.Vect[1].copy()
            self.setVect()
        self.button_more_size_check()

    def button_more_size_check(self):
        if self.PROpar.flag_rect_wind:
            self.ui.button_more_size.setIcon(self.icon_minus)
            self.ui.w_IW_size_2.show()
            #self.ui.label_size.setText("Width")
            #self.ui.label_spacing.setText("Horizontal")
            self.ui.label_size.setText("Height")
            self.ui.label_spacing.setText("Vertical")
        else:
            self.ui.button_more_size.setIcon(self.icon_plus)
            self.ui.w_IW_size_2.hide()
            self.ui.label_size.setText("Size")
            self.ui.label_spacing.setText("Spacing")

    def edit_Wind_vectors(self,wedit,wlab):
        text=wedit.text()
        split_text=re.split('(\d+)', text)[1:-1:2]
        vect=np.array([int(i) for i in split_text],dtype=np.intc)
        tip=QToolTip(wedit)
        FlagEmpty=len(vect)==0
        if FlagEmpty: FlagError=True
        else: FlagError=not np.all(vect[:-1] >= vect[1:])
        if FlagError:
            wlab.setPixmap(self.Lab_warning)
            if FlagEmpty:
                message="Please, insert at least one element!"
            else:
                message="Items must be inserted in decreasing order!"
            tip.showText(QCursor.pos(),message)
            wlab.setToolTip(message)
        else: 
            wlab.setPixmap(QPixmap())
            tip.hideText()
        self.PROpar.VectFlag[self.Vect_widgets.index(wedit)]=not FlagError
        return split_text, vect, tip, FlagError

    def set_Wind_vectors(self,wedit,wlab,i):
        def set_Wind_vectors_new():
            tip.hideText()
            if not FlagError: 
                Nit_i=len(vect) 
                if Nit_i>self.PROpar.Nit:
                    self.PROpar.Nit=Nit_i
                else:
                    if np.all(vect[:Nit_i]==self.PROpar.Vect[i][:Nit_i]):
                        self.PROpar.Nit=Nit_i    
                Vect2=[]
                for j in range(4):
                    if self.PROpar.flag_rect_wind:
                        k=j
                    else: 
                        k=j%2
                    if k==i:
                        Vect2.append(vect)
                    else:
                        Vect2.append(self.PROpar.Vect[k])      
                self.PROpar.Vect=self.adjustVect(Vect2)
            self.setVect()

        _, vect, tip, FlagError=self.edit_Wind_vectors(wedit,wlab)
        set_Wind_vectors_new() 

    def adjustVect(self,Vect):
        for i,v in enumerate(Vect):
            if self.PROpar.Nit<len(v):
                Vect[i]=v[:self.PROpar.Nit]
            elif self.PROpar.Nit>len(v):
                Vect[i]=np.append(v,np.repeat(v[-1],self.PROpar.Nit-len(v)))
        rep=np.array([0,0,0,0])
        for i,v in enumerate(Vect):
            if len(v)>1:
                while rep[i]<len(v)-1:
                    if v[-1-rep[i]]==v[-2-rep[i]]: rep[i]+=1
                    else: break
        #si potrebbe programmare meglio...
        dit=np.min(rep)
        if dit:
            self.PROpar.Nit-=dit
            for i in range(4):
                Vect[i]=Vect[i][:self.PROpar.Nit]
            self.ui.spin_final_iter.setValue(self.ui.spin_final_iter.value()+dit)
        self.setVect()
        return Vect

    def check_flag_boundary_callback(self):
        if self.ui.check_flag_boundary.isChecked():
            self.PROpar.FlagBordo=1
        else:
            self.PROpar.FlagBordo=0   
        pass

#*************************************************** FINAL ITERATIONS
    def spin_final_iter_callback(self):
        self.PROpar.NIterazioni=self.ui.spin_final_iter.value()
        self.check_more_iter()

    def check_DC_callback(self):
        if self.ui.check_DC.isChecked():
            self.PROpar.FlagDirectCorr=1
        else:
            self.PROpar.FlagDirectCorr=0
    
#*************************************************** INTERPOLATION
    def ImIntIndex2UiOptions(self,ind,w,p):
        self.Flag_setImIntIndex=False
        w.setCurrentIndex(-1) # necessary because the call to w.setCurrentIndex() evocates the callback function only if the index is changed!
        if ind==0:
            w.setCurrentIndex(w.findText(ImInt_items[0])) #none #così se scelgo un nome diverso è automatico
            self.combo_ImInt_action(w,p)
        elif ind==1: #Quad4Simplex
            w.setCurrentIndex(w.findText(ImInt_items[4]))
            self.combo_ImInt_action(w,p)
        elif ind in (3,4): #Moving S, aS
            w.setCurrentIndex(w.findText(ImInt_items[1]))
            self.combo_ImInt_action(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            qcombo.setCurrentIndex(ind-3)
        elif ind in (5,2,7,6): #BiLinear, BiQuad, BiCubic, BiCubic Matlab
            w.setCurrentIndex(w.findText(ImInt_items[3]))
            self.combo_ImInt_action(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(-1,-1,  1  ,-1,-1,  0,3,2)
            qcombo.setCurrentIndex(indeff[ind])
        elif ind==10: #Linear revitalized
            w.setCurrentIndex(w.findText(ImInt_items[2])) 
            self.combo_ImInt_action(w,p)
        elif ind>=23 and ind<=40: #Shift
            w.setCurrentIndex(w.findText(ImInt_items[5]))
            self.combo_ImInt_action(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-20)
        elif ind>=41 and ind<=50: #Sinc
            w.setCurrentIndex(w.findText(ImInt_items[6]))
            self.combo_ImInt_action(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-40)
        elif ind>=52 and ind<=70: #BSpline
            w.setCurrentIndex(w.findText(ImInt_items[7]))
            self.combo_ImInt_action(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-50)
        self.Flag_setImIntIndex=True
                  
    def ImIntUiOptions2Index(self,w,p):
        if w.currentText()==ImInt_items[0]: #none
            ind=0
        elif w.currentText()==ImInt_items[4]: #Quad4Simplex
            ind=1
        elif w.currentText()==ImInt_items[1]: #Moving S, aS
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            ind=qcombo.currentIndex()+3
        elif w.currentText()==ImInt_items[3]: #BiLinear, BiQuad, BiCubic, BiCubic Matlab
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(5,2,7,6)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==ImInt_items[2]: #Linear revitalized
            ind=10
        elif w.currentText()==ImInt_items[5]: #Shift
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+20
        elif w.currentText()==ImInt_items[6]: #Sinc 
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+40
        elif w.currentText()==ImInt_items[7]: #BSpline
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+50
        return ind

    def ImIntComboBox_selection(self,w,p):
        if w.currentText() in (ImInt_items[j] for j in(0,2,4)):
            p.setCurrentIndex(0)
        elif w.currentText()==ImInt_items[1]:
            p.setCurrentIndex(1)
        elif w.currentText()==ImInt_items[3]:
            p.setCurrentIndex(2)
        elif w.currentText() in ImInt_items[5]:
            p.setCurrentIndex(3)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Kernel width')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(3)
            qspin.setMaximum(20)
            qspin.setValue(3)
        elif w.currentText() in ImInt_items[6]:
            p.setCurrentIndex(3)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Kernel half-width')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(1)
            qspin.setMaximum(10)
            qspin.setValue(3)
        elif w.currentText() in ImInt_items[7]:
            p.setCurrentIndex(3)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Order (=Kernel width-1)')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(2)
            qspin.setMaximum(20) 
            qspin.setValue(3)
        
    def combo_ImInt_action(self,w,p):
        self.ImIntComboBox_selection(w,p)
        self.setImIntIndex(w,p)
    
    def setImIntIndex(self,w,p):
        if self.Flag_setImIntIndex:
            ind=self.ImIntUiOptions2Index(w,p)
            if w.objectName()=='combo_ImInt':
                self.PROpar.IntIniz=ind
            else:
                self.PROpar.IntFin=ind
            #self.PROpar.printPar()
        
    def VelIntIndex2UiOptions(self,ind,w,p):
        if ind>=1 and ind<=5:
            indeff=(-1,  0,2,3,4,1)
            w.setCurrentIndex(w.findText(VelInt_items[indeff[ind]])) #così se scelgo un nome diverso è automatico
            self.combo_VelInt_action(w,p)
        elif ind>=52 and ind<=70: #BSpline
            w.setCurrentIndex(w.findText(VelInt_items[5]))
            self.combo_VelInt_action(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-50)

    def VelIntUiOptions2Index(self,w,p):
        for j in range(5):    
            if w.currentText()==VelInt_items[j]: #none
                indeff=(1,5,2,3,4)
                ind=indeff[j]
                break
        if w.currentText()==VelInt_items[5]: #BSpline
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+50
        return ind

    def VelIntComboBox_selection(self,w,p):
        if w.currentText() in VelInt_items[:5]:
            p.setCurrentIndex(0)
        elif w.currentText()==VelInt_items[5]:
            p.setCurrentIndex(1)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Order (=Kernel width-1)')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(2)
            qspin.setMaximum(20)      
            qspin.setValue(3)  
        
    def combo_VelInt_action(self,w,p):
        self.VelIntComboBox_selection(w,p)
        self.setVelIntIndex(w,p)
    
    def setVelIntIndex(self,w,p):
        self.PROpar.IntVel=self.VelIntUiOptions2Index(w,p)
        #self.PROpar.printPar()

    def button_more_iter_callback(self):
        if self.PROpar.FlagInt==0:
            self.PROpar.FlagInt=1
        else:
            self.PROpar.FlagInt=0
        self.button_more_iter_check()

    def button_more_iter_check(self):
        if self.PROpar.FlagInt==0:
            self.ui.spin_final_it.setValue(self.PROpar.FlagInt)
            self.ui.button_more_iter.setIcon(self.icon_plus)
            self.ui.w_ImInt_2.hide()
            self.ui.w_ImInt_par_2.hide()
        else:
            self.ui.spin_final_it.setValue(self.PROpar.FlagInt)
            self.ui.button_more_iter.setIcon(self.icon_minus)
            self.ui.w_ImInt_2.show()
            self.ui.w_ImInt_par_2.show()

    def check_more_iter(self):
        max_it=len(self.PROpar.Vect[0])+self.PROpar.NIterazioni
        if max_it==1:
            self.PROpar.FlagInt=0
            #self.ui.button_more_iter.setEnabled(False)
            self.ui.button_more_iter.hide()
        else:
            self.ui.label_max_it.setText("of " +str(max_it))
            self.ui.spin_final_it.setMaximum(max_it-1)
            #self.ui.button_more_iter.setEnabled(True)
            self.ui.button_more_iter.show()
        if self.PROpar.FlagInt:
            self.ui.button_more_iter.setIcon(self.icon_minus)
            self.ui.w_ImInt_2.show()
            self.ui.w_ImInt_par_2.show()
        else:
            self.ui.button_more_iter.setIcon(self.icon_plus)
            self.ui.w_ImInt_2.hide()
            self.ui.w_ImInt_par_2.hide()

    def spin_final_it_callback(self):
        self.PROpar.FlagInt=self.ui.spin_final_it.value()
        #self.check_more_iter()
    
    def combo_correlation_callback(self):
        self.PROpar.IntCorr=self.ui.combo_correlation.currentIndex()
        #self.PROpar.printPar()
    
#*************************************************** VALIDATION
    def radio_MedTest_callback(self):
        if self.ui.radio_MedTest.isChecked():
            self.PROpar.FlagNogTest=0
            self.ui.radio_Nogueira.setChecked(False)
            self.PROpar.FlagMedTest=1
        else:
            self.PROpar.FlagMedTest=0
        self.showValTestBoxed()
    
    def radio_SNTest_callback(self):
        if self.ui.radio_SNTest.isChecked():
            self.PROpar.FlagNogTest=0
            self.ui.radio_Nogueira.setChecked(False)
            self.PROpar.FlagSNTest=1
        else:
            self.PROpar.FlagSNTest=0
        self.showValTestBoxed()
    
    def radio_CPTest_callback(self):
        if self.ui.radio_CPTest.isChecked():
            self.PROpar.FlagNogTest=0
            self.ui.radio_Nogueira.setChecked(False)
            self.PROpar.FlagCPTest=1
        else:
            self.PROpar.FlagCPTest=0
        self.showValTestBoxed()

    def radio_Nogueira_callback(self):
            if self.ui.radio_Nogueira.isChecked():
                self.PROpar.FlagMedTest=0
                self.ui.radio_MedTest.setChecked(False)
                self.PROpar.FlagSNTest=0
                self.ui.radio_SNTest.setChecked(False)
                self.PROpar.FlagCPTest=0
                self.ui.radio_CPTest.setChecked(False)
                self.PROpar.FlagNogTest=1
            else:
                self.PROpar.FlagNogTest=0
            self.showValTestBoxed()

    def setValidationType(self):
        self.checkValidationType()
        self.showValTestBoxed()
        self.ui.combo_MedTest_type.setCurrentIndex(self.PROpar.TypeMed)
        self.ui.spin_MedTest_ker.setValue(self.PROpar.KernMed)
        self.ui.spin_MedTest_alfa.setValue(self.PROpar.SogliaMed)
        self.ui.spin_MedTest_eps.setValue(self.PROpar.ErroreMed)
        self.ui.spin_SNTest_thres.setValue(self.PROpar.SogliaSN)
        self.ui.spin_CPTest_thres.setValue(self.PROpar.SogliaCP)
        self.ui.spin_Nog_tol.setValue(self.PROpar.SogliaMedia)
        self.ui.spin_Nog_numvec.setValue(self.PROpar.SogliaNumVet)
        
    def checkValidationType(self):
        self.ui.radio_MedTest.setChecked(self.PROpar.FlagMedTest)
        self.ui.radio_SNTest.setChecked(self.PROpar.FlagSNTest)
        self.ui.radio_CPTest.setChecked(self.PROpar.FlagCPTest)
        self.ui.radio_Nogueira.setChecked(self.PROpar.FlagNogTest)

    def showValTestBoxed(self):
        self.showMedTestwid()
        self.showSNTestwid()
        self.showCPTestwid()
        self.showNogTestwid()

    def showMedTestwid(self):
        if self.PROpar.FlagMedTest:
            self.ui.label_MedTest_box.show()
            self.ui.w_MedTest_type.show()
            self.ui.w_MedTest_ker.show()
            self.ui.w_MedTest_alfa.show()
            if self.PROpar.TypeMed==1:
                self.ui.w_MedTest_eps.show()
        else:
            self.ui.label_MedTest_box.hide()
            self.ui.w_MedTest_type.hide()
            self.ui.w_MedTest_ker.hide()
            self.ui.w_MedTest_alfa.hide()
            self.ui.w_MedTest_eps.hide()

    def showSNTestwid(self):
        if self.PROpar.FlagSNTest:
            self.ui.label_SNTest.show()
            self.ui.w_SNTest_thres.show()
        else:
            self.ui.label_SNTest.hide()
            self.ui.w_SNTest_thres.hide()

    def showCPTestwid(self):
        if self.PROpar.FlagCPTest:
            self.ui.label_CPTest.show()
            self.ui.w_CPTest_thres.show()
        else:
            self.ui.label_CPTest.hide()
            self.ui.w_CPTest_thres.hide()

    def showNogTestwid(self):
        if self.PROpar.FlagNogTest:
            self.ui.label_Nogueira.show()
            self.ui.w_Nog_tol.show()
            self.ui.w_Nog_numvec.show()
        else:
            self.ui.label_Nogueira.hide()
            self.ui.w_Nog_tol.hide()
            self.ui.w_Nog_numvec.hide()
        
    def combo_MedTest_type_callback(self):
        self.PROpar.TypeMed=self.ui.combo_MedTest_type.currentIndex()
        if self.PROpar.TypeMed==1:
            self.ui.w_MedTest_eps.show()
        else:
            self.ui.w_MedTest_eps.hide()
    
    def spin_MedTest_ker_callback(self):
        self.PROpar.KernMed=self.ui.spin_MedTest_ker.value()

    def spin_MedTest_alfa_callback(self):
        self.PROpar.SogliaMed=self.ui.spin_MedTest_alfa.value()
    
    def spin_MedTest_eps_callback(self):
        self.PROpar.ErroreMed=self.ui.spin_MedTest_eps.value()

    def spin_SNTest_thres_callback(self):
        self.PROpar.SogliaSN=self.ui.spin_SNTest_thres.value()
    
    def spin_CPTest_thres_callback(self):
        self.PROpar.SogliaCP=self.ui.spin_CPTest_thres.value()

    def spin_Nog_tol_callback(self):
        self.PROpar.SogliaMedia=self.ui.spin_Nog_tol.value()

    def spin_Nog_numvec_callback(self):
        self.PROpar.SogliaNumVet=self.ui.spin_Nog_numvec.value()

    def spin_MinVal_callback(self):
        self.PROpar.SogliaNoise=self.ui.spin_MinVal.value()
    
    def spin_MinStD_callback(self):
        self.PROpar.SogliaStd=self.ui.spin_MinStD.value()
    
    def combo_Correction_type_callback(self):
        self.PROpar.FlagCorrezioneVel=self.ui.combo_Correction_type.currentIndex()

    def check_second_peak_callback(self):
        if self.ui.check_second_peak.isChecked():
            self.PROpar.FlagSecMax=1
        else:
            self.PROpar.FlagSecMax=0
    
    def check_Hart_callback(self):
        if self.ui.check_Hart.isChecked():
            self.PROpar.FlagCorrHart=1
        else:
            self.PROpar.FlagCorrHart=0

#*************************************************** WINDOWING
    def VelWindIndex2UiOptions(self,ind,w,p):
        self.Flag_setWindIndex=False
        w.setCurrentIndex(-1)  # necessary because the call to w.setCurrentIndex() evocates the callback function only if the index is changed!
        if ind in (0,3,4):          # top-hat
            w.setCurrentIndex(w.findText(Wind_items[0]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(0, -1,-1, 1, 2)
            qcombo.setCurrentIndex(indeff[ind])
        elif ind in (1,21):         # Nogueira
            w.setCurrentIndex(w.findText(Wind_items[1]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            if ind==1:
                qcombo.setCurrentIndex(0)
            else:
                qcombo.setCurrentIndex(1)
        elif ind in (5,2,6):        # Blackman
            w.setCurrentIndex(w.findText(Wind_items[2]))
            self.combo_Wind_callback(w,p)
            """
            #Blackman options
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(-1,-1, 1, -1,-1, 0,2)
            qcombo.setCurrentIndex(indeff[ind])
            """
        elif ind in (7,8,9,10):     # Blackman-Harris
            w.setCurrentIndex(w.findText(Wind_items[3]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            qcombo.setCurrentIndex(ind-7)
        elif ind==22:               # Triangular
            w.setCurrentIndex(w.findText(Wind_items[4]))
            self.combo_Wind_callback(w,p)
        elif ind==23:               # Hann
            w.setCurrentIndex(w.findText(Wind_items[5]))
            self.combo_Wind_callback(w,p)
        elif ind>=100 and ind<=200: #Gaussian
            w.setCurrentIndex(w.findText(Wind_items[6]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(MyQDoubleSpin)
            qspin.setValue(float(ind-100)/10)
        self.Flag_setWindIndex=True

    def WindUiOptions2Index(self,w,p):
        if w.currentText()==Wind_items[0]:     # top-hat/rectangular
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(0,3,4)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[1]:   # Nogueira
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(1,21)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[2]:   # Blackman
            """
            #Blackman options
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(5,2,6)
            ind=indeff[qcombo.currentIndex()]
            """
            ind=2
        elif w.currentText()==Wind_items[3]:   # Blackman-Harris
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(7,8,9,10)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[4]:   # Triangular
            ind=22
        elif w.currentText()==Wind_items[5]:   # Hann
            ind=23
        elif w.currentText()==Wind_items[6]:   # Gaussian
            q=p.widget(p.currentIndex())
            qspin=q.findChild(MyQDoubleSpin)
            ind=int(qspin.value()*10+100)
        return ind
        
    def WindCombo_Selection(self,w,p):
        if Flag_type_of_DCs:
            if w.objectName()=='combo_Wind_Corr_type':
                if w.currentText()==Wind_items[0]: 
                    self.ui.w_type_of_DCs.hide()
                else: 
                    self.ui.w_type_of_DCs.show()
        for i in range(4):
            if w.currentText()==Wind_items[i] and i!=2:  #!!! Blackman options: delete i!=2 and 2 from in(2,4,5) below (triang./Hann)
                p.show()
                p.setCurrentIndex(i+1)
                break
        if w.currentText() in (Wind_items[j] for j in(2,4,5)): #triang./Hann no parameters needed
            p.hide()
        if w.currentText()==Wind_items[6]:
            p.show()
            p.setCurrentIndex(5)
        
    def combo_Wind_callback(self,w,p):
        self.WindCombo_Selection(w,p)
        self.setWindIndex(w,p)
            
    def setWindIndex(self,w,p):
        if self.Flag_setWindIndex:
            ind=self.WindUiOptions2Index(w,p)
            if w.objectName()=='combo_Wind_Vel_type':
                self.PROpar.FlagCalcVel=ind
            else:
                self.PROpar.FlagWindowing=ind
            #self.PROpar.printPar()

    def spin_Wind_halfwidth_callback(self):
        self.PROpar.SemiDimCalcVel=self.ui.spin_Wind_halfwidth.value()

    def radio_Adaptative_callback(self):
        if self.ui.radio_Adaptative.isChecked():
            self.PROpar.FlagAdaptative=1
            self.ui.w_Adaptative.show() 
            self.ui.w_adaptative_iter.show()
            self.ui.combo_Wind_Vel_type.setCurrentIndex(1)
            self.ui.combo_Wind_Corr_type.setCurrentIndex(1)
            self.ui.spin_Wind_halfwidth.setValue(1)
            self.PROpar.FlagCalcVel=self.ui.combo_Wind_Vel_type.currentIndex() 
            self.PROpar.FlagWindowing=self.ui.combo_Wind_Corr_type.currentIndex()
            self.PROpar.SemiDimCalcVel=self.ui.spin_Wind_halfwidth.value()
            FlagEnabled=False
        else:
            self.PROpar.FlagAdaptative=0
            self.ui.w_Adaptative.hide()
            self.ui.w_adaptative_iter.hide()
            FlagEnabled=True
        
        self.ui.combo_Wind_Vel_type.setEnabled(FlagEnabled)
        self.ui.combo_Wind_Corr_type.setEnabled(FlagEnabled)
        self.ui.spin_Wind_halfwidth.setEnabled(FlagEnabled)

    def spin_adaptative_iter_callback(self):
        self.PROpar.NItAdaptative=self.ui.spin_adaptative_iter.value()

    def spin_min_Corr_callback(self):
        self.PROpar.MinC=self.ui.spin_min_Corr.value()
        self.ui.spin_max_Corr.setMinimum(self.PROpar.MinC+0.01)
        
    def spin_max_Corr_callback(self):
        self.PROpar.MaxC=self.ui.spin_max_Corr.value()
        self.ui.spin_min_Corr.setMaximum(self.PROpar.MaxC-0.01)
    
    def spin_min_Lar_callback(self):
        self.PROpar.LarMin=self.ui.spin_min_Lar.value()
        self.ui.spin_max_Lar.setMinimum(self.PROpar.LarMin+1)
        
    def spin_max_Lar_callback(self):
        self.PROpar.LarMax=self.ui.spin_max_Lar.value()
        self.ui.spin_min_Lar.setMaximum(self.PROpar.LarMax-1)
    
    def combo_type_of_DCs_callback(self):
        self.PROpar.FlagSommaProd=self.ui.combo_type_of_DCs.currentIndex()


if __name__ == "__main__":
    import sys
    app=QApplication.instance()
    if not app:app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Process_Tab(None)
    object.show()
    app.exec()
    app.quit()
    app=None
