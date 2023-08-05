import anytree
import pandas as pd
from anytree import RenderTree, findall, ZigZagGroupIter
from ..BBG.core import BDH

pd.set_option('display.max_columns', None)

class Node(anytree.Node):
    '''
    THIS EXPANDS THE NODE CLASS IN THE ANYTREE LIBRARY WITH THE FOLLOWING FUNCTIONALITY:
    adding: node1 + node2 will calculate the union sets and return a tuple with the resulting (asset_ids,asset_names)
    subtracting: node1 - node2 will return a tuple of the (asset_ids, asset_names) in node1 so long as they dont appear in node2
    render: node.render() will perform a basic rendering of such node, all the way downwards
    '''
    def __add__(self,other):
        asset_ids=self.asset_ids.copy()
        for asset_id in other.asset_ids:
            if not(asset_id in asset_ids):
                asset_ids+=[asset_id]
        temp_node = Node(name="temp",parent=None)
        temp_node.asset_ids = asset_ids
        return temp_node

    def __sub__(self, other):
        asset_ids=[]
        for asset_id in self.asset_ids:
            if not(asset_id in other.asset_ids):
                asset_ids+=[asset_id]
        temp_node = Node(name="temp",parent=None)
        temp_node.asset_ids = asset_ids
        return temp_node


    def render(self,sort=True,show_aggregate = False,aggregate_digits=7):

        #define sort function - whether by name of the node or, if we have additional_printout, by additional_printout
        def mysort(items):
            if sort:
                if show_aggregate:
                    return sorted(items, key=lambda item: item.aggregate, reverse=True)
                else:
                    return sorted(items, key=lambda item: item.name, reverse=False)
            else:
                return items

        #iterate
        for pre, _, node in RenderTree(self,childiter=mysort):
            if show_aggregate:
                exec(f"global _addon;_addon = ''+str(node.aggregate)+'  '")
                _addon_format = "%" + str(int(aggregate_digits)) + "s"
            else:
                _addon_format="%s"
                exec(f"global _addon;_addon = ''")
            print(("%s"+_addon_format+"%s") % (pre, _addon,node.name))

    def search(self, node_name, partial_match=False, first_result=True, verbose=False):
        '''
        :param node_name: string to search for
        :param partial_match: if True, will return nodes that contain the node_name. If false, it will only bring exact matches
        :param first_result: if True, only returns one result
        :param verbose: if True, will print number of search results alongside asset count
        :return: single Node or tuple of Nodes depending on the options. If no results found, then None.
        '''
        if partial_match:
            found = findall(self, filter_=lambda node: node_name in node.name)
        else:
            found = findall(self, filter_=lambda node: node.name in [node_name])
        if verbose:
            print(f"{len(found)} results found")
            for node in found:
                print(node.name + f"---- {len(node.asset_ids)} assets")
            if len(found)>1 and first_result:
                print("returning first match only")
        if len(found)>0:
            if first_result or len(found)==1:
                return found[0]
            else:
                return found
        else:
            return None

    def custom_aggregate(self,aggregate_field="",aggregate_function="sum", filter_fields=[], filter_values=[],propagate=False,verbose=True):
        '''
        :param aggregate_field: eg "max_occupancy", must be one of numeric fields in the configuration_df (--> INTERNAL CONFIG DATA!!!)
        :param aggregate_function: "sum", "max", etc.
        :param filter_fields: [list of configuration df columns to filter by]
        :param filter_values:[list of filter values]
        :param propagate: if True, it will create for this node and all branches below a new property node.aggregate with the outcome of the computation at node level (eg max capacity)
        :return: aggregate for the parent node (although it will also have updated node.aggregate and all the subnodes.aggregate. It will also inherit data through all subnodes!
        '''

        #if propagate is True we create a tuple with levels of nodes
        if propagate==True:
            zigzag = [node for node in ZigZagGroupIter(self)]
        else:
            zigzag = [[self]]
        for level in reversed(zigzag):
            for node in level:
                # ensure it has data (NOTE - THIS WILL ONLY WORK IF DATA HAS BEEN LOADED FIRST)
                if node != self:
                    try:
                        node.inherit_data(self)
                    except:
                        pass
                #calculate custom aggregate
                df = node.root.configuration_df.copy()
                df = df[(df[node.asset_id_field].isin(node.asset_ids))]
                for filter_name,filter_value in zip(filter_fields,filter_values):
                    df = df[df[filter_name]==filter_value]
                exec ("global _custom_aggregate_output;_custom_aggregate_output = df['"+aggregate_field+"']."+aggregate_function+"()")
                if verbose:
                    print(f"{node.name} {aggregate_field} {aggregate_function} = {_custom_aggregate_output}")
                if propagate:
                    node.aggregate = _custom_aggregate_output

        return _custom_aggregate_output


    def load_params(self,params_dict):
        '''
        :param params_dict: format as per the below
            params_dict = {
                "listSecID":["AAPL US Equity"],
                "listFieldID":["PX_LAST","BEST_PE_RATIO"],
                "listFieldScale":[],
                "startDateYYYYMMDD":"20220701",
                "endDateYYYYMMDD":"20230131",
                "periodicityAdjustment":"ACTUAL","periodicitySelection":"DAILY","maxDataPoints":0,
                "overrides":[],
                "convertDatesToNumbers":False,
                "oneTablePer":"SECURITY",
                "onlyCommonDates":True,
                "return_as_dict":False
                }
        :return: it creates a self.params attribute that can be accessed further, for instance self.params.startDateYYYYMMDD.
        It also creates for each telemetry a self.data.TEMPERATURE (for instance) where the list of downloaded dfs per asset will be stored
        '''
        self.params = Params(params_dict)
        self.data = Data(self.params,len(self.asset_ids))
        return self


    def load_data(self):
        '''
        needs to have loaded params first!
        assumes one table per security & concat = False
        :return: each telemetry will have a list of dfs corresponding to the data downloaded for each asset in self.asset_ids
        '''
        temp_df = BDH(
            listSecID=self.params.listSecID,
            listFieldID=self.params.listFieldID,
            listFieldScale=self.params.listFieldScale,
            startDateYYYYMMDD=self.params.startDateYYYYMMDD,
            endDateYYYYMMDD=self.params.endDateYYYYMMDD,
            periodicityAdjustment=self.params.periodicityAdjustment,
            periodicitySelection=self.params.periodicitySelection,
            listOverrides=[],
            maxDataPoints = self.params.maxDataPoints,
            convertDatesToNumbers = self.params.convertDatesToNumbers,
            oneTablePer="SECURITY",
            onlyCommonDates=self.params.onlyCommonDates,
            return_as_dict=False)

        for df in temp_df:
            for field in self.params.listFieldID:
                relevant_cols = [col for col in temp_df.columns if ("_"+field) in col]
                temp_df_metric = temp_df.copy()[relevant_cols]
                temp_df_metric.columns = ["_".join(x.split("_")[:-1]) for x in temp_df_metric.columns]
                exec("self.data." + field + "[" + str(i) + "]=temp_df_metric")
                if len(temp_df_metric)==0:
                    print(f"Data not found for asset {asset_id} ({field}")
            return self

    def inherit_data(self,data_node):
        self.params = data_node.params
        self.data = Data(self.params,len(self.asset_ids))
        for telemetry in [attribute for attribute in dir(data_node.data) if not attribute.startswith('__')]:
            exec(f"parent_dict = data_node.{telemetry}")
            for i,asset_id in zip(range(0,len(self.asset_ids)),self.asset_ids):
                if asset_id in data_node.asset_ids:
                    exec("self.data."+telemetry+"[i] = parent_dict[asset_id]")


    def __if_no_children_then_condense(space, telemetry, operation):
        if len(space.children) == 0:
            sum_of_assets = space.merge_data(telemetry, operation)
            sum_of_assets.columns = [space.name + "_condensed"]

            space.condensed = [sum_of_assets]
        else:
            space.condensed = []
            for child in space.children:
                space.condensed += child.condensed

    def condense(root_node, telemetry, operation):
        '''
        :param root_node: the top level node we want to condense all the way down
        :param telemetry: "AREA_COUNT" etc
        :param operation: "sum", "max", "min", "etc"
        :return: it modifies every node from root_node downwards by adding the .condensed property with a df ofor each of the leaf spaces (not assets) under it
        '''
        #this creates a tuple with levels of nodes
        zigzag = [node for node in ZigZagGroupIter(root_node)]
        for level in reversed(zigzag):
            for node in level:
                # ensure it has data
                if node != root_node:
                    node.inherit_data(root_node)

                #if there are only assets under it, not further children spaces, then it aggregates all asset data into one
                if len(node.children) == 0:
                    sum_of_assets = node.merge_data(telemetry, operation)
                    sum_of_assets.columns = [node.name + "_condensed"]
                    node.condensed = [sum_of_assets]
                else:
                    #if it has space children, it creates a list of all the condensed spaces below it
                    node.condensed = []
                    for child in node.children:
                        node.condensed += child.condensed

    def merge_data(self, telemetry, transform_function="plain", use_asset_names=False, filter_fields=[], filter_values=[]):
        '''
        :param telemetry: single telemetry (eg "AREA_COUNT")
        :param transform_function: "plain" if we want asset by asset results, any of the pandas functions ("sum", "min", "max", "median" etc) if not. Applied horizontally to all assets.
        :param use_asset_names: if True, it will return asset names instead of asset ids as columns
        :param configuration_df: optional - if we want to filter by attribute name and value, this df will contain asset_id plus the attribute names
        :param filter_fields: list of attribute names (columns of configuration_df) we want to filter by
        :param filter_values: list of attribute values we want to filter by. All need to match concurrently.
        :return: df with the resulting data, and where the columns are either asset names ("plain") or telemetry_operation (eg "AREA_COUNT_sum")
        '''
        global _combined_df
        df_list=[]
        for asset_id, asset_df in zip(self.asset_ids,self.__text_to_property(telemetry)):
            if asset_df is None:
                pass
            else:
                df_list+=[asset_df]

        #*****30-08-22 add filtering*****
        configuration_df = self.root.configuration_df
        if configuration_df is None:
            pass
        else:
            for attribute_name, attribute_value in zip(filter_fields, filter_values):
                configuration_df = configuration_df[configuration_df[attribute_name]==attribute_value]
            eligible_assets = [str(asset) for asset in list(configuration_df["asset_id"])]
            df_list = [df for df in df_list if str(df.columns[0]) in eligible_assets]
        # *****30-08-22 add filtering*****

        if len(df_list)>0:
            _combined_df = pd.concat(df_list,axis=1)
            _combined_df.index.name=telemetry
            if transform_function!="plain":
                exec("global _combined_df;_combined_df = _combined_df."+transform_function+"(axis=1).to_frame()")
                _combined_df.columns=[telemetry+"_"+transform_function]
            if use_asset_names and transform_function=="plain":
                cols = list(_combined_df.columns)
                new_cols = []
                id_to_name_dictionary = res = {str(self.asset_ids[i]): self.asset_names[i] for i in range(len(self.asset_ids))}
                for i in range(0,len(cols)):
                    new_cols+=[id_to_name_dictionary[str(cols[i])]]
                _combined_df.columns=new_cols
            return _combined_df
        else:
            return None

    def __text_to_property(self,property_name):
        print(self.name)
        exec("global temp;temp=self.data."+property_name)
        return temp


    # *******************11-09-2022**************

class Params:
    def __init__(self,params_dict):
        self.params_dict = params_dict
        for parameter in params_dict:
            exec("self."+parameter+"=params_dict[parameter]")
class Data:
    def __init__(self,params,num_assets):
        for field in params.listFieldID:
            exec("self."+field+"=[None]*"+str(num_assets))



def create_tree(configuration_df,levels,initial_depth,asset_id_field="",add_asset_ids=False):
    '''
    :param configuration_df: a df containing asset names and ids plus whatever fields we deem appropriate for accordion classification. Must have the columns asset_name and asset_id
    :param levels: a list with the names of the grouping columns we want to generate the tree from, eg levels=["building","group","level_01","level_02","level_03"]
    :param initial_depth: the level we want to start the tree at (e.g. in the example above depth=0 starts with "building"
    :param add_asset_ids: if True, it will add asset ID at the end of each node
    :return: a list of the root Nodes of the tree
    '''
    global id
    id = 0
    global return_nodes
    return_nodes=[]
    def __recursive_tree(df,levels,initial_depth,parent=None,add_asset_ids=False):
        global id
        depth=initial_depth
        level=levels[0:depth+1]
        idx = df.groupby(level,dropna=True).indices
        if (len(idx)==0) and (add_asset_ids==True):
            for asset_id in parent.asset_ids:
                id=id+1
                asset_node = Node(name=str(asset_id),parent=parent)
                asset_node.asset_id_field = asset_id_field
                exec("global ID"+str(id)+";ID"+str(id)+"=asset_node")

        for item in idx:
            if type(item)==str:
                new_node=item
            else:
                new_node=item[-1]
            new_df=df[df[levels[depth]]==new_node]
            if asset_id_field!="":
                asset_id_list = list(new_df[asset_id_field])
            else:
                asset_id_list=[]
            node = Node(new_node,
                        parent=parent,
                        asset_ids=asset_id_list)
            node.asset_id_field = asset_id_field
            exec("global ID"+str(id)+";ID"+str(id)+"=node")
            if parent==None:
                exec("global ID"+str(id)+";return_nodes+=[ID"+str(id)+"]")

            id=id+1
            if (depth+1)<len(levels):
                __recursive_tree(df=new_df,levels=levels,initial_depth=depth+1,parent=node,add_asset_ids=add_asset_ids)

    __recursive_tree(df=configuration_df,levels=levels,initial_depth=initial_depth,parent=None,add_asset_ids=add_asset_ids)
    # 2022-09-10
    for node in return_nodes:
        node.configuration_df = configuration_df
        node.levels = levels
    #***********
    return return_nodes



