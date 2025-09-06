import subprocess

def ka9q_metadump(control='hf.local', ssrc="7074000"):
    """
    Capture a snapshot of a ka9q-radio channel's status using metadump,
    and convert it to a dictionary.
    """

    _cmd = f"metadump -n -s {ssrc} {control}"

    _metadump = subprocess.getoutput(_cmd)

    _output = {}

    # Process metadump output line by line
    for line in _metadump.split('\n'):

        # Source Description
        if line.startswith('[4]'):
            _output['description'] = line[4:]

        elif line.startswith('[98] rf gain'):
            _output['rf_gain'] = float(line.split()[3])

        elif line.startswith('[97] rf atten'):
            _output['rf_atten'] = float(line.split()[3])

        elif line.startswith('[110] rf level cal'):
            _output['rf_level_cal'] = float(line.split()[4])

        elif line.startswith('[45] IF pwr'):
            _output['if_power'] = float(line.split()[3])

        elif line.startswith('[104] A/D overrange:'):
            _output['ad_over'] = int(line.split()[3].replace(',',''))


    return _output




if __name__ == "__main__":

    print(ka9q_metadump())
