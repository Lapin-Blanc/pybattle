Blockly.JavaScript['simulation_loop'] = function(block) {
  var statements_simulation_code = Blockly.JavaScript.statementToCode(block, 'simulation_code');
  var code = `importScripts('lib/tank.js');
tank.init(function(settings, info) {

})
tank.loop(function(state, control) {\n` +
  statements_simulation_code + '});\n';
  return code;
};

Blockly.JavaScript['update_control'] = function(block) {
  var dropdown_control = block.getFieldValue('control');
  var value_value = Blockly.JavaScript.valueToCode(block, 'value', Blockly.JavaScript.ORDER_ATOMIC);
  var code = 'control.' + dropdown_control + ' = ' + value_value +';\n';
  return code;
};

Blockly.JavaScript['input_position'] = function(block) {
  var dropdown_position = block.getFieldValue('position');
  // TODO: Assemble JavaScript into code variable.
  var code = 'state.' + dropdown_position;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['state_radar'] = function(block) {
  var dropdown_radar = block.getFieldValue('radar');
  // TODO: Assemble JavaScript into code variable.
  var code;
  if (dropdown_radar == 'angle') {
      code = 'state.radar.angle';
  } else { // dropdown = 'wallDistance'
      code = 'state.radar.wallDistance ? state.radar.wallDistance : Infinity';
  }
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['shoot'] = function(block) {
  var value_power = Blockly.JavaScript.valueToCode(block, 'POWER', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = 'control.SHOOT = ' + value_power + '\n';
  return code;
};
