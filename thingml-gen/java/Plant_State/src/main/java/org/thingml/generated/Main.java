/**
 * File generated by the ThingML IDE
 * /!\Do not edit this file/!\
 * In case of a bug in the generated code,
 * please submit an issue on our GitHub
 **/

package org.thingml.generated;

import no.sintef.jasm.*;
import no.sintef.jasm.ext.*;

import org.thingml.generated.api.*;
import org.thingml.generated.messages.*;

import java.util.*;

//import org.thingml.generated.network.*;
public class Main {
    // Things
    public static TimerJava TimerJava_timer;
    public static MQTTDriver MQTTDriver_T1;
    public static PIM PIM_pim;

    public static void main(String args[]) {
        // Things
        TimerJava_timer = (TimerJava) new TimerJava();
        TimerJava_timer.buildBehavior(null, null);
        TimerJava_timer.init();
        MQTTDriver_T1 = (MQTTDriver) new MQTTDriver();
        MQTTDriver_T1.buildBehavior(null, null);
        MQTTDriver_T1.init();
        PIM_pim = (PIM) new PIM();
        PIM_pim.buildBehavior(null, null);
        PIM_pim.init();
        // Connecting internal ports...
        // Connectors
        TimerJava_timer.getTimer_port().addListener(PIM_pim.getTimer_port());
        PIM_pim.getTimer_port().addListener(TimerJava_timer.getTimer_port());
        PIM_pim.getTo_psm_port().addListener(MQTTDriver_T1.getFrom_pim_port());
        MQTTDriver_T1.getTo_pim_port().addListener(PIM_pim.getFrom_psm_port());
        TimerJava_timer.initTimerJava_timer_var((java.util.Timer) null);
        TimerJava_timer.initTimerJava_timer_task_var((java.util.TimerTask) null);
        PIM_pim.initPIM_number_of_sections_var((int) (2));
        PIM_pim.initPIM_current_plant_state_var((String) null);
        PIM_pim.initPIM_current_side_camera_height_var((double) 0.0d);
        PIM_pim.initPIM_current_light_green_pixel_count_var((double) 0.0d);
        PIM_pim.initPIM_current_green_pixel_count_var((double) 0.0d);
        PIM_pim.initPIM_current_dark_green_pixel_count_var((double) 0.0d);
        PIM_pim.initPIM_current_red_pixel_count_var((double) 0.0d);
        PIM_pim.initPIM_current_white_pixel_count_var((double) 0.0d);
        PIM_pim.initPIM_current_yellow_pixel_count_var((double) 0.0d);
        PIM_pim.initPIM_section_id_var((int) (0));
        PIM_pim.initPIM_fruit_threshhold_var((double) (10));
        // Network components for external connectors
        /* $NETWORK$ */
        // External Connectors
        /* $EXT CONNECTORS$ */
        /* $START$ */
        TimerJava_timer.start();
        PIM_pim.start();
        MQTTDriver_T1.start();
        // Hook to stop instances following client/server dependencies (clients firsts)
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                MQTTDriver_T1.stop();
                PIM_pim.stop();
                TimerJava_timer.stop();
                /* $STOP$ */
            }
        });

    }
}