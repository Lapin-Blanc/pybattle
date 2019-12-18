Blockly.Blocks['simulation_loop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Répète indéfiniment");
    this.appendStatementInput("simulation_code")
        .setCheck(null);
    this.setInputsInline(false);
    this.setColour(120);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['update_control'] = {
  init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Régler")
        .appendField(new Blockly.FieldDropdown([["vitesse","THROTTLE"], ["rotation du char","TURN"], ["rotation du radar","RADAR_TURN"], ["rotation du canon","GUN_TURN"]]), "control")
        .appendField("à ");
    this.appendValueInput("value")
        .setCheck("Number");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("Les valeurs doivent être comprises entre entre -1 et 1");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['input_position'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["position horizontale","x"], ["position verticale","y"], ["position angle","angle"]]), "position");
    this.setOutput(true, "Number");
    this.setColour(20);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['state_radar'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["radar : angle","angle"], ["radar : distance du mur","wallDistance"]]), "radar");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(20);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['shoot'] = {
  init: function() {
    this.appendValueInput("POWER")
        .setCheck("Number")
        .appendField("Tire des obus de taille");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(330);
 this.setTooltip("Tire avec une puissance comprise entre 0.1 et 1");
 this.setHelpUrl("");
  }
};
