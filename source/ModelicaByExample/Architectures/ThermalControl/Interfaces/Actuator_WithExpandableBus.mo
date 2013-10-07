within ModelicaByExample.Architectures.ThermalControl.Interfaces;
partial model Actuator_WithExpandableBus
  "Actuator subsystem interface with an expandable bus"

  Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b furnace
    "Connection point for the furnace"
    annotation (Placement(transformation(extent={{90,-10},{110,10}})));
  ExpandableBus bus
    annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
  annotation (Diagram(graphics), Icon(graphics));
end Actuator_WithExpandableBus;
