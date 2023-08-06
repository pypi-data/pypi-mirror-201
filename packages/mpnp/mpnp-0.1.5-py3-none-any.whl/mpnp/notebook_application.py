get_ipython().run_line_magic('matplotlib', 'widget')
import matplotlib

from IPython.display import display
import ipywidgets as widgets
from tkinter import Tk
from tkinter import filedialog
from vaxm import VAX
import numpy as np
from tkinter import messagebox
import matplotlib.pyplot as plt











class Vax_App( ):


    def __init__( self, file_name = None, X = None, y = None, X_emb = None, instance_names = None, **kwargs ):

        
        self.output = widgets.Output()

        self.jeps_vis = display( display_id = 'jeps_vis' )
        self.maps_vis = display( display_id = 'maps_vis' )
        self.tooltip_vis = display( display_id = 'tooltip_vis' )

        self.porder = self.vorder = self.coverage = self.range_frame = self.label_angle = self.label_size = self.left = self.right = self.top = self.bottom = None

        self.file_name = ''
        self.dtm = self.exp = self.patterns = None
        self.X = self.x_k = self.instance_names = self.y = self.X_emb = None
        self.k_old = -1
        self.fig = self.ax = None

        self.svg_args = { 'draw_row_labels' : True, 'draw_col_labels' : True, 'draw_rows_line' : False, 'draw_cols_line' : False, 'col_label_degrees' : 15, 'draw_box_frame' : False, 'inner_pad_row' : 5, 'inner_pad_col' : 5, 'cell_background' : 'all', 'cell_background_color' : '#f2f2f2',  'draw_frame_top_legend' : False, 'draw_box_row_left_legend' : True, 'draw_frame_left_legend' : False, 'rows_left_legend_show_value' : True, 'draw_frame_right_legend' : False, 'draw_box_row_right_legend' : False, 'rows_right_legend_width' : 75/3, 'binary_legend' : [ '< 0.05', '>= 0.05' ], 'margin_left' : 400, 'margin_top' : 650, 'margin_right' : 400, 'margin_bottom' : 300, 'matrix_legend_ratio' : 0.80, 'draw_range_box' : False, 'draw_x_k' : False, 'col_label_font_size' : 25 }

        for i in kwargs: self.svg_args[ i ] = kwargs[ i ]

        self.svg_args0 = self.svg_args.copy()
        


        # open_file = widgets.Button( description = "Open File" )
        self.save = widgets.Button( description = "Save" )

        self.porder = widgets.Dropdown( options = [ ('none', 1), ('support', 2), ('class & support', 3) ], value = 2, description = 'Patterns By:', layout = {'width': 'max-content'} ) # starts with 'support'

        self.vorder = widgets.Dropdown( options = [ ('none', 1), ('importance', 2) ], value = 2, description = 'Variables By:', layout = {'width': 'max-content'} ) # starts with 'importance'

        self.coverage = widgets.FloatSlider( value = 0.0, min = 0, max = 100.0, step = 0.05, description = 'Coverage:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = '.2f' )
        
        self.range_frame = widgets.Checkbox( value = self.svg_args[ 'draw_range_box' ], description = 'Range', disabled = False, indent = False )

        self.label_angle = widgets.IntSlider( value = self.svg_args[ 'col_label_degrees' ], min = 0, max = 90, step = 1, description = 'Angle:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = 'd' ) # , layout = widgets.Layout( width = '350px')

        self.label_size = widgets.IntSlider( value = self.svg_args[ 'col_label_font_size' ], min = 0, max = 35, step = 1, description = 'Size:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = 'd' ) # , layout = widgets.Layout( width = '300px')
        
        self.left = widgets.IntSlider( value = self.svg_args[ 'margin_left' ], min = 0, max = 1000, step = 5, description = 'Left:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = 'd' )
        
        self.top = widgets.IntSlider( value = self.svg_args[ 'margin_top' ], min = 0, max = 1000, step = 5, description = 'Top:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = 'd' )
        
        self.right = widgets.IntSlider( value = self.svg_args[ 'margin_right' ], min = 0, max = 1000, step = 5, description = 'Right:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = 'd' )
        
        self.bottom = widgets.IntSlider( value = self.svg_args[ 'margin_bottom' ], min = 0, max = 1000, step = 5, description = 'Bottom:', disabled = False, continuous_update = False, orientation = 'horizontal', readout = True, readout_format = 'd' )

        self.reset = widgets.Button( description = "Reset" )



        self.tab = widgets.Tab()
        self.tab.children = [ widgets.HBox( [ self.porder, self.vorder, self.coverage, self.range_frame ] ), widgets.HBox( [ self.label_angle, self.label_size ] ), widgets.HBox( [ self.left, self.right, self.top, self.bottom ] ), widgets.HBox( [ self.save, self.reset ] ) ]
        self.tab.set_title( 0, 'Main' )
        self.tab.set_title( 1, 'Feature Name' )
        self.tab.set_title( 2, 'Margin' )
        self.tab.set_title( 3, 'Save & Reset' )
        display( self.tab, self.output )
            
        
        
        self.jeps_vis.display( '< JEPs >' )
        # self.maps_vis.display( '< MAPs >' )


        
        if file_name != None:        
            self.file_name = file_name
            self.jeps()

            
            
        if ( X_emb is not None ) and ( y is not None ):
            self.X_emb = X_emb
            self.y = y
            self.maps()



        if ( X is not None ):        
            self.X = X

            
        
        if ( instance_names is not None ):        
            self.instance_names = instance_names

        self.tooltip_vis.display( '< >' )
            
        
        
        self.porder.observe( self.order_filter_f2 )
        self.vorder.observe( self.order_filter_f1 )
        self.coverage.observe( self.order_filter_f2 )
        self.range_frame.observe( self.order_filter_f1 )
        self.label_angle.observe( self.order_filter_f1 )
        self.label_size.observe( self.order_filter_f1 )
        self.left.observe( self.order_filter_f1 )
        self.right.observe( self.order_filter_f1 )
        self.top.observe( self.order_filter_f1 )
        self.bottom.observe( self.order_filter_f1 )
        self.reset.on_click( self.reset_f )
        self.save.on_click( self.save_figures_f )











    def open_file_f( self, b ):
            
        
        Tk().withdraw() 
        file_name = filedialog.askopenfilename( title = 'Open VAX csv file ...', initialdir = './', filetypes = [ ( 'VAX csv file', '*.csv' ) ] )

        if self.file_name != '':

            self.file_name = file_name.replace( '.csv', '' )            
            self.jeps_vis.update( 'JEPs' )

            self.dtm = None
            self.jeps()
            
            

            
            






    def jeps( self ):
        
            
        if self.dtm == None:        
            self.dtm = VAX( verbose = 0 )
            self.dtm.load( self.file_name )
        
        r_order = 'raw'
        if self.porder.label != 'none': r_order = self.porder.label
        
        f_order = 'raw'
        if self.vorder.label != 'none': f_order = self.vorder.label
            
        self.svg_args[ 'draw_range_box' ] = self.range_frame.value
        
        self.svg_args[ 'margin_left' ] = self.left.value
        self.svg_args[ 'margin_right' ] = self.right.value
        self.svg_args[ 'margin_top' ] = self.top.value
        self.svg_args[ 'margin_bottom' ] = self.bottom.value

        self.svg_args[ 'col_label_degrees' ] = self.label_angle.value

        self.svg_args[ 'col_label_font_size' ] = self.label_size.value
            
            
            
        if ( self.patterns is not None ) and ( len( self.patterns ) == 0 ):
            
            self.jeps_vis.update( '< JEPS >, Select an instance or Reset.' )
            
        else:
        
        
            # try:



            if self.patterns is None: # start and reset

                self.exp = self.dtm.explanation( r_order = r_order, f_order = f_order, draw_distribution = True, show_feature_importance = True, show_info_text = False ) # r_order starts with 'support'

                self.patterns = self.exp.rules_[ :2 ].tolist() # the 2 highest support patterns

                self.coverage.value = ( self.dtm.rules_matrix_[ self.patterns[ 0 ], self.dtm.COVERAGE ] + self.dtm.rules_matrix_[ self.patterns[ 1 ], self.dtm.COVERAGE ] + 0.01 ) * 100

                self.exp = self.dtm.explanation( rules = np.array( self.patterns ), f_order = f_order, draw_distribution = True, show_feature_importance = True, show_info_text = False )

            else:

                if self.coverage.disabled == False:

                    data_coverage_max = self.coverage.value / 100.00

                    self.exp = self.dtm.explanation( r_order = r_order, f_order = f_order, data_coverage_max = data_coverage_max, draw_distribution = True, show_feature_importance = True, show_info_text = False )

                    self.patterns = self.exp.rules_.tolist()

                else:

                    self.exp = self.dtm.explanation( rules = np.array( self.patterns ), r_order = r_order, f_order = f_order, x_k = self.x_k, draw_distribution = True, show_feature_importance = True, show_info_text = False )

                    self.patterns = self.exp.rules_.tolist()


            
            if self.x_k is None: self.svg_args[ 'draw_x_k' ] = False
            else: self.svg_args[ 'draw_x_k' ] = True

            self.exp.create_svg( **self.svg_args )
            self.jeps_vis.update( self.exp.display_jn() )


            
            # except Exception as e:

            #     Tk().withdraw() 
            #     messagebox.showinfo( "Error",  str( e ) )







            

            
            
    def on_pick( self, event ):


        k = event.ind[ 0 ]

    
        if event.mouseevent.button == 1:
            
        
            if( self.coverage.disabled == False ):

                self.coverage.disabled = True
                self.coverage.value = 0.0

            
            p = self.dtm.instances_map_[ :, k ].nonzero()[ 0 ][ 0 ]
            
            if p not in self.patterns:
                
                self.patterns.append( p )
                
                if( self.instance_names is not None ):
                    self.tooltip_vis.update( self.instance_names[ k ] + ', pattern p' + str( p + 1 ) )
                else:
                    self.tooltip_vis.update( 'instance ' + str( k ) + ', pattern p' + str( p + 1 ) )

            else:
                
                self.patterns.remove( p )

                self.tooltip_vis.update( '< >' )

            
            self.jeps()
            self.maps()
            
            
        elif ( event.mouseevent.button == 2 ) and ( self.X is not None):


            if( self.coverage.disabled == False ):

                self.coverage.disabled = True
                self.coverage.value = 0.0

            
            if( k != self.k_old ):

                self.x_k = self.X[ k, : ]

                p = self.dtm.instances_map_[ :, k ].nonzero()[ 0 ][ 0 ]

                if p not in self.patterns: self.patterns.append( p )

                if( self.instance_names is not None ):
                    self.tooltip_vis.update( self.instance_names[ k ] + ', pattern p' + str( p + 1 ) )
                else:
                    self.tooltip_vis.update( 'instance ' + str( k ) + ', pattern p' + str( p + 1 ) )

                self.k_old = k

            else: 

                self.x_k = None

                self.tooltip_vis.update( '< >' )

                self.k_old = -1

            
            self.jeps()
            self.maps()


        elif event.mouseevent.button == 3:
            
            
            p = self.dtm.instances_map_[ :, k ].nonzero()[ 0 ][ 0 ]
            
            if( self.instance_names is not None ):
                self.tooltip_vis.update( 'Pattern ' + str( p + 1) + ': ' + np.array2string( self.instance_names[ self.dtm.instances_map_[ p, : ].nonzero()[ 1 ] ], max_line_width = 1000, separator = ',' ) )
            else:
                self.tooltip_vis.update( 'Pattern ' + str( p + 1) + ': instances ' + np.array2string( self.dtm.instances_map_[ p, : ].nonzero()[ 1 ], max_line_width = 1000, separator = ',' ) )






            
            
        


    def maps( self ):
        
        
        if( self.fig is None ) and ( self.ax is None ):
            
            self.fig, self.ax = plt.subplots( nrows = 1, ncols = 2, figsize = ( 9.5, 3 ) )
            
        else:
            
            self.ax[ 0 ].clear()
            self.ax[ 1 ].clear()
            
        
        # fig.canvas.toolbar_visible = False
        self.fig.canvas.toolbar_position = 'right'
        self.fig.canvas.header_visible = False
        self.fig.canvas.footer_visible = False
        self.fig.canvas.callbacks.connect( 'pick_event', self.on_pick )
        
        
        ss = 6
        if len( self.patterns ) < ss: patterns_s = self.patterns
        else: patterns_s = self.patterns[ :ss ]
        
        
        # self.dtm.plot_map( self.X_emb, self.y, np.array( patterns_s ), plt, self.fig, self.ax, font_legend_size = 8, size = 30, linewidth = 0.45, color_map1 = np.array( [ '#f2f2f2ff', '#1f77b3', '#ff7e0e', '#bcbc21' ] ), color_map2 = np.array( [ '#f2f2f2ff', '#e277c1', '#9367bc', '#bc0049', '#00aa79', '#ffdb00', '#d89c00', '#e41a1c', '#8c564b', '#ff9a75' ] ) ) # first version with colors fixed
        self.dtm.plot_map( self.X_emb, self.y, np.array( patterns_s ), plt, self.fig, self.ax, font_legend_size = 8, size = 30, linewidth = 0.45 )
        
        # plt.ioff()
        plt.tight_layout()
        # plt.show()






                
            

            
            
    def save_figures_f( self, b ):

            
        Tk().withdraw() 
        file_name_s = filedialog.asksaveasfilename( title = 'Save figures ...', initialdir = './', filetypes = [ ( 'PNG', '*.png' ), ( 'SVG', '*.svg' ) ] )

        if file_name_s != '':

            img_type = file_name_s[-3:]            
            file_name_s = file_name_s.replace( '.' + img_type, '' )

            if img_type == 'png':

                self.exp.save( file_name_s + '-JEPs.png', pixel_scale = 5 )

                if( self.X_emb is not None ) and ( self.y is not None ):
                    self.fig.savefig( file_name_s + '-MAPs.png', dpi = 300, bbox_inches = 'tight' )

            elif img_type == 'svg':

                self.exp.save( file_name_s + '-JEPs.svg' )
                if( self.X_emb is not None ) and ( self.y is not None ):
                    self.fig.savefig( file_name_s + '-MAPs.svg', bbox_inches = 'tight' )

     



         
        
        
        


    def order_filter_f1( self, change ): # update jeps
        self.jeps()
        
        
    def order_filter_f2( self, change ): # update jeps and maps    
        self.jeps()    
        if ( self.X_emb is not None ) and ( self.y is not None ):
            self.maps()





            
            
            
            
            
    def reset_f( self, b ):


        self.porder.unobserve( self.order_filter_f2 )
        self.vorder.unobserve( self.order_filter_f1 )
        self.coverage.unobserve( self.order_filter_f2 )
        self.range_frame.unobserve( self.order_filter_f1 )
        self.label_angle.unobserve( self.order_filter_f1 )
        self.label_size.unobserve( self.order_filter_f1 )
        self.left.unobserve( self.order_filter_f1 )
        self.right.unobserve( self.order_filter_f1 )
        self.top.unobserve( self.order_filter_f1 )
        self.bottom.unobserve( self.order_filter_f1 )
        self.reset.unobserve( self.reset_f )
        self.save.unobserve( self.save_figures_f )



        self.svg_args = self.svg_args0.copy()

        self.x_k = None
        self.k_old = -1

        self.left.value = self.svg_args[ 'margin_left' ]
        self.right.value = self.svg_args[ 'margin_right' ]
        self.top.value = self.svg_args[ 'margin_top' ]
        self.bottom.value = self.svg_args[ 'margin_bottom' ]

        self.label_angle.value = self.svg_args[ 'col_label_degrees' ]
        self.label_size.value = self.svg_args[ 'col_label_font_size' ]
        
        self.porder.value = 2 # if 'self.porder.value' change, 'order_filter_f1()' will be called, and by that, 'jeps()'   
        self.vorder.value = 2 # if 'vorder.value' change, 'order_filter_f1()' will be called, and by that, 'jeps()'
        
        self.patterns = None
        self.tooltip_vis.update( '< >' )
        
        self.coverage.value = 0.0 # if 'coverage.value' change, 'order_filter_f2()' will be called, and by that, 'jeps()'
        if self.coverage.disabled == True: self.coverage.disabled = False
            
        self.range_frame.value = self.svg_args[ 'draw_range_box' ]



        self.porder.observe( self.order_filter_f2 )
        self.vorder.observe( self.order_filter_f1 )
        self.coverage.observe( self.order_filter_f2 )
        self.range_frame.observe( self.order_filter_f1 )
        self.label_angle.observe( self.order_filter_f1 )
        self.label_size.observe( self.order_filter_f1 )
        self.left.observe( self.order_filter_f1 )
        self.right.observe( self.order_filter_f1 )
        self.top.observe( self.order_filter_f1 )
        self.bottom.observe( self.order_filter_f1 )
        self.reset.on_click( self.reset_f )
        self.save.on_click( self.save_figures_f )



        self.jeps()
        self.maps()

