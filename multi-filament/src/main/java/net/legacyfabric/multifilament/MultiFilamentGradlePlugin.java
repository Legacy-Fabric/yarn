package net.legacyfabric.multifilament;

import org.gradle.api.Plugin;
import org.gradle.api.Project;
import org.gradle.api.tasks.TaskContainer;

import net.fabricmc.filament.task.CombineUnpickDefinitionsTask;

import net.legacyfabric.multifilament.task.FixedRemapUnpickDefinitionsTask;

public class MultiFilamentGradlePlugin implements Plugin<Project> {
	@Override
	public void apply(Project project) {
		TaskContainer tasks = project.getTasks();
		CombineUnpickDefinitionsTask combineUnpickDefinitions = (CombineUnpickDefinitionsTask) tasks.getByName("combineUnpickDefinitions");
		tasks.register("fixedRemapUnpickDefinitionsIntermediary", FixedRemapUnpickDefinitionsTask.class, (task) -> {
			task.setGroup("multi-filament");
			task.dependsOn(combineUnpickDefinitions);
			task.getInput().set(combineUnpickDefinitions.getOutput());
			task.getSourceNamespace().set("named");
			task.getTargetNamespace().set("intermediary");
		});
	}
}
