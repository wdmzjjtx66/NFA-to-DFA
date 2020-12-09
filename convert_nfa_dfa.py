"""
Input file should be similar as follows, the following lines should be from a .json file.
Following are some examples for nfa_input.json file.

Example 1
{
  "nfa_states": 3,
  "nfa_symbols": ["a", "b"],
  "sigma_function": [[0, "a", [0, 1]], [0, "b", [0]], [1, "b", [2]]],
  "start_state": 0,
  "final_state":  [2]
}

Example 2
{
  "nfa_states": 2,
  "nfa_symbols": ["a", "b"],
  "sigma_function": [[0, "a", [0, 1]], [0, "b", [1]], [1, "b", [0, 1]]],
  "start_state": 0,
  "final_state":  [1]
}

Example 3
{
  "nfa_states": 3,
  "nfa_symbols": ["a", "b"],
  "sigma_function": [[0, "a", [0]], [0, "b", [1]], [1, "a", [1, 2]], [1, "b", [1]], [2, "a", [2]], [2, "b", [1, 2]]],
  "start_state": 0,
  "final_state":  [2]
}
"""


from collections import OrderedDict

# We use the json format as our input and output file format, because it is a perfect file type for dictionary data structure
import json
with open('nfa_input.json') as file:
    data = json.load(file)


# Import and record number of NFA states, set of transition symbols, and start state
# DFA input symbols will be the same as NFA input symbols
# DFA start state will be the same as NFA start state
dfa_symbols = data["nfa_symbols"]
dfa_start_state = data["start_state"]


# Start from step 1 and step 2, add the start state into set Q'
Q_set = []
Q_set.append((dfa_start_state,))


# Import and record the transition rules for NFA machine
nfa_trans = {}
for trans in data["sigma_function"]:
    nfa_trans[(trans[0], trans[1])] = trans[2]


# Step 3 and step 4, iteratively add and expand states set and transitions for DFA, if we haven't seen it before.
dfa_trans = {}

# Iterate through the state-symbol pair in the Q', add new states set into Q' when we never seen it before.
for input_state in Q_set:
    for symbol in dfa_symbols:

        # Adding state-symbol pair transition from NFA to DFA if the input state is already in NFA (not a newly formed state)
        if len(input_state) == 1 and (input_state[0], symbol) in nfa_trans:

            # Mapping the DFA output of state-symbol pair same as NFA output for the same pair
            dfa_trans[(input_state, symbol)] = nfa_trans[(input_state[0], symbol)]

            # If we haven't seen this input state-symbol pair before, we should add the output of this pair into Q', as this output would be the newly formed state in DFA
            if tuple(dfa_trans[(input_state, symbol)],) not in Q_set:
                Q_set.append(tuple(dfa_trans[(input_state, symbol)]),)

        # else we got a newly-formed state or we never saw this input state-symbol pair before
        else:
            output_set = []
            # For each state in the newly-formed state, adding the NFA output states to the output set, if we haven't add it yet
            # Then we will combine all output states as a newly formed states and add it to Q' later
            for n_state in input_state:
                if (n_state, symbol) in nfa_trans and nfa_trans[(n_state, symbol)] not in output_set:
                    output_set.append(nfa_trans[(n_state, symbol)])

            # For each output state in dest, we should add it to the output states set for the current input state-symbol pair, and append it to Q' if we never see this output state before
            output_set_combined = []
            if output_set:
                for i in output_set:
                    for j in i:
                        if j not in output_set_combined:
                            output_set_combined.append(j)

                dfa_trans[(input_state, symbol)] = list(sorted(output_set_combined))
                if tuple(sorted(output_set_combined),) not in Q_set:
                    Q_set.append(tuple(sorted(output_set_combined),))


# Compute the total number of states in DFA
dfa_states = set()
for given, out in dfa_trans.items():
    temp_s = given[0]
    if temp_s not in dfa_states:
        dfa_states.add(temp_s)
dfa_num_states = len(dfa_states)


# Add [state, input, output] of DFA to the output transition relation function
dfa_sigma = []
for given, out in dfa_trans.items():
    temp_l = [[given[0], given[1], out]]
    dfa_sigma.extend(temp_l)


# Identify and add final states for DFA. Using the rule that if a states set in DFA include some final state in NFA, we should mark it as final state for DFA
dfa_final_state = set()
for dfa_states_set in Q_set:
    for nfa_final_state in data["final_state"]:
        if nfa_final_state in dfa_states_set:
            dfa_final_state.add(dfa_states_set)
dfa_final_state = list(dfa_final_state)


# Organize the conversion results and write them to the output csv file
dfa = OrderedDict()
dfa["dfa_states"] = dfa_num_states
dfa["dfa_symbols"] = dfa_symbols
dfa["sigma_function"] = dfa_sigma
dfa["start_state"] = dfa_start_state
dfa["final_state"] = dfa_final_state

output_file = open('dfa_output.json', 'w+')
json.dump(dfa, output_file, separators=(',\t', ':'))



