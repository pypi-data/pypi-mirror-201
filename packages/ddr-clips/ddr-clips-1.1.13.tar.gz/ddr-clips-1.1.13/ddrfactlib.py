from pprint import pprint as pp
import copy
import clips
import xml.dom.minidom
import xml.etree.ElementTree as ET
import xmltodict



def test_get_template_multifacts_index(env, fact_template, slot, device_name, device_index, get_response):
        '''
            Use a NETCONF get operation to read operational or configuration model content.
            If the data is in a list, create a fact for each list entry optionally filtered using a list of key names.
            Extract identified leaf values for the response and insert into the facts

            {"fact_type": "multitemplate",
            "data": ["multitemplate", 0, "CAT9K-24", # fact type, index into device_list, device name
            """<interfaces xmlns='http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper'> # cut and paste from a YANG view of the model (suggest use YangSuite)
                    <interface>
                      <name/>
                      <statistics>
                        <in-errors/>
                        <in-crc-errors/>
                        <in-errors-64/>
                      </statistics>
                    </interface>
                  </interfaces>""",
            "interface-stats", "interface", #first element is fact template name, 2nd element is list name given by user
            ["name", "in-errors", "in-crc-errors", "in-errors-64"], # names of leafs that end in /> generated if /> at end
            [["name", "str"], ["in-errors", "int"], ["in-crc-errors", "int"], ["in-errors-64", "int"]], # names of the slots in the interface-stats fact generate deftemplate slot names with same values as leaf names
            [['fact-name1', 'value1'], ['fact-name2', 'value2']], # list of facts to assert when this template is executed
            ['GigabitEthernet1', 'GigabitEthernet2']] # list of key filters, only return data if key (name) matches a list entry
            }

            :param fact: List of parameters used to control fact collection
               [0] - Fact type
               [1] - device_list index for device to perform operation
               [2] - device name to include in generated fact
               [3] - RPC content for get operation to get the required leafs
               [4] - name of deftemplate for the fact that will be generated
               [5] - name of the 'key' leaf.  One fact will be generated for each instance of the key
               [6] - parameter names in the RPC which will be extracted and asserted as slots in the fact
               [7] - slot names in the deftemplate to receive the parameters extracted from the get result
               [8] - optional list of additional facts to assert when this template is executed
               [9] - list of key values to use as filters to generate facts only for keys that match the list, if empty [] generate facts for all keys
        
        Usage::

              get_template_multifacts_index(self, test_fact, device, 'CAT9K-24', 0)

            :raises none:

        '''

        fact = fact_template["data"]
        path =  fact[3]
        deftemplate = fact[4]
        key = fact[5]
        leafs = fact[6]  
        facts = fact[7]
        assert_list = fact[8] # list of facts to assert when this template is executed
        element_list = fact[9]
        try:
    #
    # If there are facts that must be asserted for this call assert all facts in the required templates
    # The list contains entries of this form [[template_name, slot_name, slot_value]]
    #
            for assert_fact in assert_list:
                try:
                    env.assert_string("(" + str(assert_fact[0]) + " (" + str(assert_fact[1]) + " " + str(assert_fact[2]) + "))")
                except: pass #ignore case where FACT already exists
    #
    # get data for multiple instances
    # instances will be a list of the objects which match the "key"
    #
            instances = xml.dom.minidom.parseString(get_response).getElementsByTagName(key)
    #
    # Filter entries in multitemplate list if a filter is specified to limit fact collection
    #
            if element_list != []:
                filtered_elements = []
                filtered_instances = []
                for each in instances:
                    instance = []
                    fact = facts[0]
                    if fact[1] == 'str':
                        for node in each.getElementsByTagName(fact[0]):
                            if str(node.firstChild.nodeValue).replace(" ", "") in element_list:
                                filtered_elements.append(str(node.firstChild.nodeValue).replace(" ", ""))
                                filtered_instances.append(each)
                    if fact[1] == 'int':
                        for node in each.getElementsByTagName(fact[0]):
                            if int(node.firstChild.nodeValue) in element_list:
                                filtered_elements.append(int(node.firstChild.nodeValue))
                                filtered_instances.append(each)
                element_list = filtered_elements
                instances = filtered_instances

            instance_list = []
            for each in instances:
                instance = []
                for leaf in leafs:
    #
    # If no value is returned for the get request the value is []
    # A value of 'nil' must be filled in if no value is returned from the get request
    #
                    if len(each.getElementsByTagName(leaf)) == 0:
                        instance.append('nil')
                    else:
                        for node in each.getElementsByTagName(leaf):
                            instance.append(node.firstChild.nodeValue)
                if instance != []:
                    instance_list.append(instance)
                instance = []
    #
    # For each instance in the instance_list assert the information read as facts
    # Create a python dictionary with each key:value pair where the key is the slot
    # and value is the slot value
    # Template facts may specify the type of the value stored into the slot
    #  [["five-seconds", "int"], ["one-minute", "int"], ["five-minutes", "int"]]
    #
            for each in instance_list:
                template = env.find_template(str(deftemplate))
                fact1 = {}
                fact1["device"] = str(device_name)
                j = 0

                try:
                    for fact in facts:
                        if len(fact) == 2:
                            if fact[1] == "int":
                                fact1[str(fact[0])] = int(each[j])
                            elif fact[1] == "str":
                                fact1[str(fact[0])] = str(each[j]).replace(" ", "_")
                            elif fact[1] == "flt":
                                fact1[str(fact[0])] = float(each[j])
                            else:
                                print("%%%% DDR Exception: Invalid fact type " + str(fact))
                                break

                            j = j + 1
                        
                        else:
                            if isinstance(each[j], int):
                                fact1[str(fact)] = int(each[j])
                            else:
                                fact1[str(fact)] = str(each[j]).replace(" ", "_")
                                j = j + 1
                except Exception as e:
                    print("\n%%%% DDR Error: get_template_multifacts fact generation error: " + str(fact))                      
    #
    # Assert the FACT defined by a Python dictionary
    #
                try:
                    template.assert_fact(**fact1)
                except Exception as e:
                    print("%%%% DDR Exception: get_template_multifacts_index assert_fact: " + str(e))

        except Exception as e:
            print("\n%%%% DDR Error: get_template_multifacts_index error: " + str(e))
            print("\n%%%% DDR Error: No value found in get_template_multifacts_index: " + str(fact1))
        return


def get_netconf_fact(fact, test_rpc, env, deftemplate):

            get_result = test_rpc
            instances = xml.dom.minidom.parseString(get_result).getElementsByTagName(key)
    #
    # Filter entries in multitemplate list if a filter is specified to limit fact collection
    #
            if element_list != []:
                filtered_elements = []
                filtered_instances = []
                for each in instances:
                    instance = []
                    fact = facts[0]
                    if fact[1] == 'str':
                        for node in each.getElementsByTagName(fact[0]):
                            if str(node.firstChild.nodeValue).replace(" ", "") in element_list:
                                filtered_elements.append(str(node.firstChild.nodeValue).replace(" ", ""))
                                filtered_instances.append(each)
                    if fact[1] == 'int':
                        for node in each.getElementsByTagName(fact[0]):
                            if int(node.firstChild.nodeValue) in element_list:
                                filtered_elements.append(int(node.firstChild.nodeValue))
                                filtered_instances.append(each)
                element_list = filtered_elements
                instances = filtered_instances

            instance_list = []
            for each in instances:
                instance = []
                for leaf in leafs:
                    for node in each.getElementsByTagName(leaf):
                        instance.append(node.firstChild.nodeValue)
                if instance != []:
                    instance_list.append(instance)
                instance = []
    #
    # For each instance in the instance_list assert the information read as facts
    # Create a python dictionary with each key:value pair where the key is the slot
    # and value is the slot value
    # Template facts may specify the type of the value stored into the slot
    #  [["five-seconds", "int"], ["one-minute", "int"], ["five-minutes", "int"]]
    #
            for each in instance_list:
                template = env.find_template(str(deftemplate))
                fact1 = {}
                fact1["device"] = str(device_name)
                j = 0
                for fact in facts:
                    if len(fact) == 2:
                        if fact[1] == "int":
                            fact1[str(fact[0])] = int(each[j])
                        elif fact[1] == "str":
                            fact1[str(fact[0])] = str(each[j]).replace(" ", "_")
                        elif fact[1] == "flt":
                            fact1[str(fact[0])] = float(each[j])
                        else:
                            break
                        j = j + 1
                        
                    else:
                        if isinstance(each[j], int):
                            fact1[str(fact)] = int(each[j])
                        else:
                            fact1[str(fact)] = str(each[j]).replace(" ", "_")
                            j = j + 1                       
    #
    # Assert the FACT defined by a Python dictionary
    #
                try:
                    template.assert_fact(**fact1)
                except Exception as e:
                    pass

            return

##############################################################################
#
#
# show_and_assert_fact - execute a show command, parse the show command output,
#            and assert a fact based on the output
#
# Example of parsed data from a show command created by a "genie_parser"
# This example shows state information for LISP instances.
# The data for the instance is a "sub_dictionary" contained in the "per_instance_dict"
# The genie_parser generates this dictionary structure
#
#            {'lisp_instance':
#               {'per_instance_dict':
#                 {'instance_id': 4100, 'lisp_id': 0, 'reg_timer': '00:02:49'}
#               }
#            }
#
# This is the FACT definition used to process the data returned by the parser
#
#  {"fact_type": "show_and_assert",
#     "command": 'show processes memory platform sorted',
#     "device": "cat9k-24",
#     "genie_parser": "ShowLispInstanceId",
#     "assert_fact_for_each_item_in": "lisp_instance",
#     "protofact": {"template": "lisp-instance",
#                                "slots": {"device": "device",
#                                          "instance": "$",
#                                          "instance-id": "$+instance_id",
#                                          "lisp-id": "$+lisp_id",
#                                          "reg-timer": "$+reg_timer"}}}

#############################################################################
def test_show_and_assert_fact(env, template, fact, response):
    try:
        #
        # use the parsed output of a show command that will be in the form of a python dictionary
        # The "fact" dictionary includes a field indentifying what part of the parsed data
        # to use to generated the CLIPs FACT
        #
        parsed_genie_output = response
        sub_dictionary_list = test_find(fact["assert_fact_for_each_item_in"], parsed_genie_output)
        import copy
        #
        # If there are multiple sets of data in the parsed response, each will be in a sub_dictionary
        # A FACT is generated for each sub_dictionary
        #
        for sub_dictionary in sub_dictionary_list:
            #
            # Each "item" in the sub_dictionary is
            # Addeded to a dictionary in the form required to generate a CLIPs FACT
            #
            for item in sub_dictionary:
                protofact = copy.deepcopy(fact["protofact"])
                for slot in protofact["slots"]:
                    value = protofact["slots"][slot]
                    #
                    # insert the device name into the fact
                    #
                    if value == "device":
                        protofact["slots"][slot] = value.replace("device", fact["device"])
                    elif type(value) == str and "$" in value:
                        protofact["slots"][slot] = value.replace("$", item)

                test_assert_template_fact(env, template, protofact, sub_dictionary)
    except Exception as e:
        print("\n&&&& show_and_assert exception: \n" + str(e))

##############################################################################
#
# find - return nested dictionary value given a dictionary (j) and a string
#		 element (element) in the form of "Garden.Flowers.White"
#
#############################################################################
def test_find(element, j):
    try:
        if element == "":
            return j
        keys = element.split('+')
        rv = j
        for i, key in enumerate(keys):
            if key == '*':
                new_list = []
                new_keys = copy.deepcopy(keys[i + 1:])  # all the keys past the * entry
                for entry in rv:  # for each entry in the * dictionary
                    new_rv = copy.deepcopy(rv[entry])
                    for new_key in new_keys:
                        new_rv = new_rv[new_key]
                    for e in new_rv:
                        new_rv[e]["upper_value"] = entry
                    new_list.append(new_rv)
                return new_list
            else:
                # normal stepping through dictionary
                try:
                   rv = rv[key]
                except Exception as e:
                    print(">> find exception: key: ", str(e), key)
                    return
        return [rv]
    except Exception as e:
        print("\n&&&& find exception: \n", str(e), element, j)


##############################################################################
#
# test_assert_template_fact - given a protofact, assert the fact into the clips system
#
# This function generates a python dictionary from the FACT data
# The python dictionary contains all of the slots that are applied to a FACT template
# The clipspy template.assert_fact method creates a CLIPs FACT using a python dictionary produced by this function
#
#############################################################################
    def test_assert_template_fact(env, template, protofact, sub_dictionary=None):
        try:
            template = env.find_template(protofact["template"])
            fact1 = {}
            for slot, value in protofact["slots"].items():
    #
    # If the "value" is in a subdirectory, look up the final value in the sub_dictionary
    #
                if type(value) is str and "+" in value:
                    value = find(value, sub_dictionary)[0]
    #
    # Use "types" in the protofact to determine the type to assert in the FACT
    #
                try:
                    if protofact["types"][slot] == "int":
                        fact1[slot] = int(value)
                    elif protofact["types"][slot] == "flt":
                        fact1[slot] = float(value)
                    else:
                        fact1[slot] = str(value).replace(" ", "_")
                except Exception as e:
                    print_log("\n%%%% DDR Error: Exception assert_template_fact: type error: " + str(e))
    #
    # Assert the FACT defined by a Python dictionary
    #
                try:
                    template.assert_fact(**fact1)
                except Exception as e:
                    print("%%%% DDR Exception: template.assert_fact: " + str(e))

        except Exception as e:
            print("\n%%%% DDR Error: Exception assert_template_fact: " + str(e))


def dummy_test_assert_template_fact(env, template, protofact):
        try:
            template = env.find_template(template)
            fact1 = {}
            for slot, value in protofact["slots"].items():
    #
    # If the "value" is in a subdirectory, look up the final value in the sub_dictionary
    #
                try:
                    if protofact["types"][slot] == "int":
                        fact1[slot] = int(value)
                    elif protofact["types"][slot] == "flt":
                        fact1[slot] = float(value)
                    else:
                        fact1[slot] = str(value).replace(" ", "_")
                except Exception as e:
                    print("%%%% DDR Exception: incorrect fact definition: " + str(value))

    #
    # Assert the FACT defined by a Python dictionary
    #
            try:
                template.assert_fact(**fact1)
            except Exception as e:
                print("%%%% DDR assert_fact Exception: assert_template_fact: " + str(e))
        except Exception as e:
            print("%%%% DDR Error: Exception test_assert_template_fact: " + str(e))

    ####################################################################################
    #
    # test_get_template_multifacts_protofact - Version of ddrclass.py function used
    #    to generate FACTs from a NETCONF get request
    #
    ###################################################################################

def test_get_template_multifacts_protofact(env, fact, template, hard_slot, hard_slot_value, get_response):
      '''
 The test_get_template_multifacts_protofact function is used in Python scripts to test the implementation
 of FACT definitions used to translate the content of NETCONF get responses into CLIPs FACTs.
 
 The get_template_multifacts_protofact function is called from the main DDR loop or when the DDR "run_nc_fact"
 function is called from a CLIPs RULE.

 The FACT dictionary entry in the nc_fact_list section of the ddr-facts file contains:
 
    "fact_type": for NETCONF operations the multitemplate_protofact is used to generate FACTs from lists in get responses

    "assert_fact_for_each": identifies the list in the response for which a FACT is generated for each list entry.
                          In the example a FACT will be generated for each DyPeer-list entry

    "element_list": {"ip": ["204.1.1.1", "201.1.1.1"]} element_list filters out FACTs and only asserts a FACT if
                   in this example, the "ip" slot in the rule contains the one of the ip addresses shown in the list.  The element_list is a dictionary
                   so additional filtering can be specified where the dictionary element key, e.g. "ip" is used to select values
                   from the list associated with the key to verify that a listed value is also present in the data.
                   If "element_list" is not included in the FACT, no filtering is performed
                          
    path: This is the path used in the NETCONF request to the device.  Optionally parameters can be inserted into
          the get request template shown in the path entry.  The parameters are defined in the run_nc_fact and
          run_nc_fact_index functions called from CLIPs rules
          In the run_nc_fact example below the arguments are as follows:
          (run_nc_fact_index 3 ?device 1 ?edId none none)
          3 - Index in to the nc_fact_list in the ddr-facts file for the FACT definition to use
          ?device - A variable used to select which device to access
          1 - Indicates the number of parameters to insert into the "path" (0, 1, 2, or 3)
          ?epId - Variable that will be inserted into the "path" to replace {0} (note parameter 2 replaces {1} and 3 replaces {2})
          none - No value for this optional parameter
          
    protofact: This entry describes how to extract data from the get_response and where to insert the data
               into the FACT.  
               "template:" is the name of the deftemplate definition in the ddr-rules file
               The left-hand entry in "slots:" defines the slots or fields in the deftemplate that will recieve the data
               The right-hand entry defines how to extract the data from the get_response.
               In the definition below "nve": 'Ep-list/epId' selects the value of the epId in the Ep-list in the
               get_response and places the value in an nve-peer-list FACT in the nve slot.
               "primary-ip" and "admin-state" are also selected from the Ep-list.
               The next 3 slot definitions ip, state, mac, because there is no "list-name/" are used to create
               a FACT for each entry in the DyPeer-list.
               
    types: This second defines the type for each value that will be populated into the FACT.

 For the example get_response and fact_list entry below, the following FACTs are generated:

    (nve-peer-list (tname nve-peer-list) (device "n9k") (nve 1) (admin-state "enabled") (primary-ip "204.1.1.1") (peer-ip "201.1.1.1") (peer-state "Up") (peer-mac "00:00:00:00:00:00"))
    (nve-peer-list (tname nve-peer-list) (device "n9k") (nve 1) (admin-state "enabled") (primary-ip "204.1.1.1") (peer-ip "1.2.3.4") (peer-state "Down") (peer-mac "10:00:00:00:00:00"))
nc_fact_list = [
{"fact_type": "multitemplate_protofact", 
        "device_index": 0,
        "device": 'n9k-test-1',
        "assert_fact_for_each": 'DyPeer-list',
        "hardcoded_list": ["device"],
        "element_list": {"peer-ip": ["1.2.3.5", "201.1.1.1"], "peer-mac": ["00:00:00:00:00:00", "10:00:00:00:00:00"]},

"path": '
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <eps-items>
          <epId-items>
            <Ep-list>
              <epId>{0}</epId>
              <adminSt/>
              <primaryIp/>
              <peers-items>
                <dy_peer-items>
                  <DyPeer-list>
                    <ip/>
                    <state/>
                    <mac/>
                  </DyPeer-list>
                </dy_peer-items>
              </peers-items>
            </Ep-list>
          </epId-items>
        </eps-items>
      </System>',
"protofact": {"template": 'nve-peer-list',
              "slots": {"device": 'None',
                        "nve": 'Ep-list/epId',
                        "primary-ip": 'Ep-list/primaryIp',
                        "admin-state": 'Ep-list/adminSt',
                        "peer-ip": 'ip',
                        "peer-state": 'state',
                        "peer-mac": 'mac'
                       },
              "types": {"device": 'str',
                        "nve": 'int',
                        "primary-ip": 'str',
                        "admin-state": 'str',
                        "peer-ip": 'str',
                        "peer-state": 'str',
                        "peer-mac": 'str'
                        } 
        }
}
]
      '''

      try:
        get_result = get_response

        # Create a list of all instances in the XML response includes an instance of a list with the name in: fact["assert_fact_for_each"]
        
        instances = xml.dom.minidom.parseString(get_result).getElementsByTagName(fact["assert_fact_for_each"])

        # The instances in the response that will be used to generate FACTs can be filtered
        # If the fact definition includes a dictionary key "filtered_instances" the following code includes
        # only instances where the value in the selected slot matches a valued in "filtered_instances"
        # For example: "element_list": {"peer-ip": ["1.2.3.5", "201.1.1.1"], "peer-mac": ["00:00:00:00:00:00", "10:00:00:00:00:00"]},
        # FACTs will only be generated if the FACT contains one of the listed peer-ip AND one of the listed peer-mac
        # 
        if "element_list" in fact:
            filtered_instances = []
            for each in instances:
                found = False
                slots = fact['protofact']["slots"]
                for slot in slots:
                    if found: break
                    if ("hardcoded_list" in fact) and (slot in fact["hardcoded_list"]): continue
                    node_list = each.getElementsByTagName(slots[slot])
                    if node_list:
                        node = node_list[0]
                    elif "/" in slots[slot]:
                        node = get_upper_value(each, slots[slot])
                    else: continue
                    for category in fact["element_list"]:
                        if slot == category:
                            if (str(node.firstChild.nodeValue).replace(" ", "") in fact["element_list"][category]):
                                filtered_instances.append(each)
                                found = True
                                break
        else:
            filtered_instances = instances

        # Generate a FACT for each instance in the get_response
        # The protofact element in the FACT dictionary is copied and the slot values read from the get_response are
        # written into the copy of the protofact dictionary
        # For example, after execution the new "protofact" variable could contain:
        #
        #    protofact: {'template': 'nve-peer-list', 'slots': {'device': 'n9k', 'nve': 1, 'primary-ip': '204.1.1.1', 'admin-state': 'enabled', 'peer-ip': '201.1.1.1', 'peer-state': 'Up', 'peer-mac': '00:00:00:00:00:00'}
        #
        # The protofact dictionary generated below is used to assert the FACT into CLIPs
        #
        for each in filtered_instances:
            protofact = copy.deepcopy(fact['protofact'])
            slots = fact['protofact']["slots"] # list of slots (fields) that will have values assigned
            for slot in slots:

                # The "device" dictionary element defined in the FACT definition or the "hard_slot_value" function parameter
                # can be inserted into the device slot in the FACT

                if ("hardcoded_list" in fact) and (slot == fact["hardcoded_list"][0]):
                    if (hard_slot_value == None): # Get the slot value from the FACT definition
                        protofact["slots"][slot] = fact["device"]                
                        continue
                    else: # Get the slot value passed in by the function call 'hard_slot_value'
                        protofact["slots"][slot] = hard_slot_value                
                        continue

                # create a list XML nodes that for the "slot" in the FACT, for example "ip"
                # There will only be one element in the list
                # If the value has a / then a second lookup is required to get value 'Ep-list/primaryIp'

                node_list = each.getElementsByTagName(slots[slot])
                if node_list:
                    node = node_list[0]
                elif "/" in slots[slot]:
                    # for upper tags, node_list would have been empty above
                    node = get_upper_value(each, slots[slot])
                else: continue

                # use the xml library to get the conents of the leaf in the model for example ip address "204.1.1.1"
                value = node.firstChild.nodeValue

                # set the type of value saved in the protofact dictionary using the types defined in the FACT section "types"
                
                if protofact["types"][slot] == "int":
                    protofact["slots"][slot] = int(value)
                elif protofact["types"][slot] == "flt":
                    protofact["slots"][slot] = float(value)
                else:
                    protofact["slots"][slot] = str(value).replace(" ", "_")
    #
    # Assert the FACT in the CLIPs instance using the deftemplate "template"
    # and the FACT content (protofact) generated above.  For example:
    #    protofact: {'template': 'nve-peer-list', 'slots': {'device': 'n9k', 'nve': 1, 'primary-ip': '204.1.1.1', 'admin-state': 'enabled', 'peer-ip': '201.1.1.1', 'peer-state': 'Up', 'peer-mac': '00:00:00:00:00:00'}
    # CLIPs provides a function that asserts a FACT using the content of a dictionary
    #
            dummy_test_assert_template_fact(env, template, protofact)
            print("**** DDR Debug: protofact: " + str(protofact) + "\n")

        return
      except Exception as e:
          print("\n%%%% DDR Error: get_template_multifacts_protofact_index: " + str(e))
          
    ##############################################################################
    #
    # get_upper_value - Get the value for model nodes above the target nodes
    #                   These nodes are normally keys in a nested list above the
    #                   target nodes
    #
    ##############################################################################
def get_upper_value(node, upper_tag_key_combo):
        tag_key_list = upper_tag_key_combo.split("/")
        upper_tag = tag_key_list[0]
        key = tag_key_list[1]
        cur_node = node
        while cur_node.tagName != upper_tag:
            try:
                cur_node = cur_node.parentNode
            except:
                print("\n%%%% DDR Error: Protofact could not find parent: " + str(upper_tag_key_combo))
                return
        return cur_node.getElementsByTagName(key)[0]

